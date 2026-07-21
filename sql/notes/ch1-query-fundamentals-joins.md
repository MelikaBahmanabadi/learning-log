# Chapter 1 — Query Fundamentals & Joins

**Sources:** SQL Cookbook (Molinaro/de Graaf), SQL Performance Explained (Winand)

---

## 1. Relational Model Refresher

A **relation** is a set of tuples. A **table** is a concrete representation. Key terms:

| Term | Meaning |
|------|---------|
| Cardinality | Number of rows in a relation |
| Degree | Number of columns |
| Candidate key | Minimal set of columns that uniquely identifies a row |
| Primary key | Chosen candidate key |
| Foreign key | Columns referencing another table's primary key |
| Domain | Allowable set of values for a column |

**Why this matters for interviews:** You must distinguish between a table (implementation) and a relation (mathematical concept). SQL tables can have duplicates; relations cannot. The `SELECT DISTINCT` exists because SQL operates on *bags*, not sets.

---

## 2. SQL Execution Order

SQL is **not** read top-to-bottom. The logical order:

```
1. FROM        — identify source tables
2. JOIN        — combine tables
3. WHERE       — filter rows (before aggregation)
4. GROUP BY    — group remaining rows
5. HAVING      — filter groups (after aggregation)
6. SELECT      — compute columns
7. DISTINCT    — remove duplicate rows
8. ORDER BY    — sort
9. LIMIT/OFFSET — restrict output
```

**Critical insight:** You cannot reference a `SELECT` alias in `WHERE`. The alias is computed *after* the WHERE filter.

```sql
-- WRONG — alias doesn't exist yet at WHERE stage
SELECT salary * 12 AS annual_salary
FROM employees
WHERE annual_salary > 100000;

-- CORRECT
SELECT salary * 12 AS annual_salary
FROM employees
WHERE salary * 12 > 100000;

-- Or use HAVING (only for aggregates) or subquery/CTE
SELECT annual_salary
FROM (
  SELECT salary * 12 AS annual_salary FROM employees
) sub
WHERE annual_salary > 100000;
```

---

## 3. JOIN Types — Visual Mental Model

### INNER JOIN
Keeps only rows that match in **both** tables.

```sql
SELECT o.order_id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
```

### LEFT (OUTER) JOIN
Keeps all rows from the **left** table. NULLs fill unmatched right side.

```sql
-- All customers, even those with no orders
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
```

### RIGHT (OUTER) JOIN
Mirror of LEFT JOIN. Rarely used — just swap table order.

### FULL (OUTER) JOIN
Keeps all rows from **both** tables. NULLs fill gaps on either side.

```sql
-- Customers without orders AND orders without valid customers
SELECT c.name, o.order_id
FROM customers c
FULL OUTER JOIN orders o ON c.id = o.customer_id;
```

### CROSS JOIN
Cartesian product — every row from A paired with every row from B.

```sql
-- 10 customers × 3 products = 30 rows
SELECT c.name, p.product_name
FROM customers c
CROSS JOIN products p;
```

**Use case:** Generating combinations (e.g., every user × every feature flag).

### SELF JOIN
Join a table to itself — useful for hierarchies and comparisons.

```sql
-- Find employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Find pairs of employees in the same department
SELECT a.name, b.name, a.department_id
FROM employees a
JOIN employees b ON a.department_id = b.department_id
  AND a.id < b.id;  -- avoid duplicates and self-pairs
```

---

## 4. Join Algorithms (Performance Explained)

Understanding how databases *execute* joins is key for interviews and optimization.

### Nested Loop Join
```
for each row in outer:
    scan inner table for matches
```
- **Good when:** outer is small, inner has an index on join column
- **Cost:** O(N × M) without index, O(N × log M) with index
- **Used by:** all databases as a fallback, especially for small datasets

### Hash Join
```
1. Build hash table from smaller table on join key
2. Probe hash table with each row from larger table
```
- **Good when:** both tables large, no useful index
- **Cost:** O(N + M)
- **Used by:** PostgreSQL, Oracle, SQL Server for large joins

### Merge Join (Sort-Merge)
```
1. Sort both tables on join key
2. Walk both sorted streams in parallel
```
- **Good when:** inputs are already sorted (e.g., from an index scan)
- **Cost:** O(N log N + M log M), or O(N + M) if pre-sorted
- **Used by:** PostgreSQL (when order guaranteed), Oracle

**Interview question:** *"When would the optimizer choose a nested loop over a hash join?"*
→ When the outer input is very small (or already filtered to few rows), the index lookup cost per row is cheap, and building a hash table is overkill.

---

## 5. Correlated Subqueries vs. Joins

### Correlated Subquery
References the outer query — executes **once per row**.

```sql
-- Find employees who earn more than their department average
SELECT e.name, e.salary, e.department_id
FROM employees e
WHERE e.salary > (
  SELECT AVG(salary)
  FROM employees e2
  WHERE e2.department_id = e.department_id  -- correlated!
);
```

### Equivalent JOIN with GROUP BY

```sql
SELECT e.name, e.salary, e.department_id
FROM employees e
JOIN (
  SELECT department_id, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department_id
) dept_avg ON e.department_id = dept_avg.department_id
WHERE e.salary > dept_avg.avg_salary;
```

**Which is better?** It depends:
- PostgreSQL can optimize `WHERE x IN (SELECT ...)` into joins via "pull-up"
- MySQL historically struggles with correlated subqueries (use JOINs)
- Modern optimizers often produce the same plan for both

### EXISTS vs. IN

```sql
-- Find customers who placed at least one order
-- EXISTS (short-circuits on first match)
SELECT c.name FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- IN (materializes full subquery result first)
SELECT c.name FROM customers c
WHERE c.id IN (
  SELECT customer_id FROM orders
);
```

| | EXISTS | IN |
|---|--------|----|
| Behavior | Correlated — checks per row | Materializes subquery first |
| NULL handling | Correct (NULLs don't match) | Tricky — `NULL IN (NULL)` is `UNKNOWN` |
| Performance | Better when subquery is indexed | Better when subquery is small and finite |
| DB dependency | Works the same everywhere | `IN` with NULLs behaves differently across DBs |

**Interview tip:** Always prefer NOT EXISTS over NOT IN when the subquery column is nullable — NULL in the list silently eliminates all rows. For positive IN vs EXISTS, modern optimizers (PG 12+, MySQL 8+) often generate equivalent semi-join plans. Measure with EXPLAIN.

---

## 6. Set Operations

```sql
-- UNION: combine rows, remove duplicates
SELECT city FROM customers
UNION
SELECT city FROM suppliers;

-- UNION ALL: keep duplicates (faster — no dedup needed)
SELECT city FROM customers
UNION ALL
SELECT city FROM suppliers;

-- INTERSECT: rows in both
-- EXCEPT (or MINUS in Oracle): rows in first but not second
```

**Performance note (Performance Explained):** `UNION` requires a sort or hash for dedup. Use `UNION ALL` unless you actually need dedup — it's almost always faster.

---

## 7. Subqueries in Different Clauses

### Scalar Subquery (returns one value)
```sql
SELECT name, salary,
  salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

### Derived Table (subquery in FROM)
```sql
SELECT dept, avg_salary
FROM (
  SELECT department_id AS dept, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department_id
) sub
WHERE avg_salary > 80000;
```

### CTE (Common Table Expression)
```sql
WITH dept_stats AS (
  SELECT department_id, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department_id
)
SELECT e.name, e.salary, ds.avg_salary
FROM employees e
JOIN dept_stats ds ON e.department_id = ds.department_id;
```

**CTE vs. subquery:** Same performance in most DBs (optimizer merges them). CTEs win on readability and can be referenced multiple times. PostgreSQL supports `RECURSIVE` CTEs for graph/tree traversal.

---

## 8. NULL Semantics (Antipatterns Book)

NULL is not a value — it's a marker meaning "unknown." This creates gotchas:

```sql
-- NULL comparisons return UNKNOWN, not TRUE or FALSE
WHERE col = NULL     -- WRONG — never matches
WHERE col IS NULL    -- CORRECT

-- NULL in arithmetic propagates
1 + NULL = NULL
NULL * 0 = NULL  -- not 0!

-- NULL in aggregations
COUNT(col)     -- ignores NULLs
COUNT(*)       -- counts all rows including NULLs
SUM(col)       -- ignores NULLs, returns NULL if all NULLs

-- NULL in DISTINCT
SELECT DISTINCT col FROM t;  -- groups all NULLs together as one value

-- NULL in ORDER BY (implementation-dependent)
-- PostgreSQL/MySQL: NULLs sort LAST by default (ASC)
-- SQL Server: NULLs sort FIRST by default
-- Use NULLS FIRST / NULLS LAST explicitly
```

**Interview trap:** *"What does `WHERE x NOT IN (1, 2, NULL)` return?"*
→ **Nothing.** If `x` is anything, `x NOT IN (1, 2, NULL)` is equivalent to `x != 1 AND x != 2 AND x != NULL`. The `x != NULL` is always UNKNOWN, so the whole AND is UNKNOWN → row filtered out. **Always use `NOT EXISTS` instead.**

---

## 9. CASE Expression

```sql
-- Conditional logic in SQL
SELECT name,
  CASE
    WHEN salary >= 100000 THEN 'High'
    WHEN salary >= 60000 THEN 'Medium'
    ELSE 'Low'
  END AS salary_band
FROM employees;

-- Searced CASE (value matching)
SELECT name,
  CASE department_id
    WHEN 1 THEN 'Engineering'
    WHEN 2 THEN 'Sales'
    ELSE 'Other'
  END AS dept_name
FROM employees;

-- CASE in aggregates (pivot-like)
SELECT
  SUM(CASE WHEN department_id = 1 THEN 1 ELSE 0 END) AS eng_count,
  SUM(CASE WHEN department_id = 2 THEN 1 ELSE 0 END) AS sales_count
FROM employees;
```

---

## 10. Interview Q&A

**Q: What's the difference between WHERE and HAVING?**
A: `WHERE` filters rows *before* aggregation. `HAVING` filters groups *after* aggregation. You can use aggregate functions in HAVING but not in WHERE.

**Q: Can you use column aliases in WHERE?**
A: No. The SELECT clause is logically evaluated after WHERE. Use a subquery, CTE, or repeat the expression.

**Q: INNER JOIN vs WHERE for filtering?**
A: Functionally equivalent for simple filters. `INNER JOIN ... ON` and `WHERE` produce the same result. But semantically, ON defines how tables relate; WHERE is a post-join filter. Use ON for join conditions, WHERE for business logic.

**Q: Why is SELECT * bad in production?**
A: 1) Returns unnecessary data (bandwidth, memory), 2) Breaks if schema changes (app breaks), 3) Prevents covering index optimization (Performance Explained), 4) Makes query intent unclear.

**Q: How do you find duplicate rows?**
```sql
SELECT col1, col2, COUNT(*)
FROM table
GROUP BY col1, col2
HAVING COUNT(*) > 1;
```

**Q: What's the difference between DELETE, TRUNCATE, and DROP?**
| | DELETE | TRUNCATE | DROP |
|---|--------|----------|------|
| What | Removes specific rows | Removes all rows | Removes table + schema |
| WHERE | Yes | No | No |
| Log | Row-by-row (slow) | Minimal (fast) | Minimal |
| Triggers | Row-level triggers fire | Row-level triggers don't fire; statement-level triggers fire in PostgreSQL | N/A |
| Rollback | Yes (fully logged) | Yes in PG/SQL Server; not in MySQL by default | DB-dependent |
| Identity reset | No | Yes in SQL Server/MySQL; use RESTART IDENTITY in PG | N/A |

**Q: Explain the "no direct access to aggregation results in WHERE" rule. Give the workaround.**
A: Aggregates are computed after WHERE. Workaround: use a subquery/CTE to pre-aggregate, then filter the result.
```sql
SELECT department_id, avg_salary
FROM (
  SELECT department_id, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department_id
) sub
WHERE avg_salary > 80000;
```

**Q: When would you use a CROSS JOIN in practice?**
A: Generating all combinations — calendar × hours for scheduling, users × features for feature flag rollout, product × region for sales projections.

---

## Key Takeaways

1. SQL execution order is not what you read — understand the logical pipeline
2. NULLs break equality — use `IS NULL`, never `= NULL`; avoid `NOT IN` with nullable columns
3. Use NOT EXISTS over NOT IN (NULL trap); IN vs EXISTS is optimizer-dependent — check EXPLAIN
4. JOIN algorithms (nested loop, hash, merge) — know when each is used
5. UNION ALL over UNION unless you need dedup
6. `SELECT *` is an antipattern in production — always specify columns
