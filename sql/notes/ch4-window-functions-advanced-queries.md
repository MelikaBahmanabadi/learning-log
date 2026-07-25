# Chapter 4 — Window Functions & Advanced Queries

**Sources:** SQL Cookbook (Anthony Molinaro), SQL Performance Explained (Markus Winand)

---

## 1. Window Functions — Core Concept

**Window function** = a function that computes a value across a set of rows *related to the current row*, without collapsing them (unlike GROUP BY).

```sql
SELECT
  department,
  employee_name,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk,
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS drnk
FROM employees;
```

**Key distinction:** GROUP BY collapses rows → one output row per group. Window functions keep all input rows → each row gets a computed value based on its window frame.

**Syntax:**
```
function_name(...) OVER (
  [PARTITION BY ...]
  [ORDER BY ...]
  [ROWS/RANGE/GROUPS BETWEEN ... AND ...]
)
```

---

## 2. Ranking Functions

### 2.1 ROW_NUMBER, RANK, DENSE_RANK

| Function | Behavior with ties | Gaps? |
|----------|-------------------|-------|
| `ROW_NUMBER()` | Arbitrary order for ties | No gaps (1,2,3,4) |
| `RANK()` | Same rank for ties | Gaps (1,1,3,4) |
| `DENSE_RANK()` | Same rank for ties | No gaps (1,1,2,3) |

```sql
-- Salary ranking per department
SELECT
  employee_name,
  department,
  salary,
  ROW_NUMBER() OVER w AS row_num,  -- 1,2,3,4,5
  RANK()       OVER w AS rank_val, -- 1,2,2,4,5 (ties share rank, gaps)
  DENSE_RANK() OVER w AS dense_rnk -- 1,2,2,3,4 (ties share rank, no gaps)
FROM employees
WINDOW w AS (PARTITION BY department ORDER BY salary DESC);
```

**Use cases:**
- `ROW_NUMBER()` — pagination, deduplication (keep first/last per group)
- `RANK()` — leaderboard with ties (Olympic-style: 1, 1, 3)
- `DENSE_RANK()` — leaderboard without gaps (1, 1, 2)

**Dedup pattern (keep latest record per key):**
```sql
SELECT * FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
  FROM orders
) ranked
WHERE rn = 1;  -- latest order per user
```

### 2.2 NTILE

Splits result into N roughly equal buckets.

```sql
SELECT
  employee_name,
  salary,
  NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;
-- quartile 1 = top 25%, quartile 4 = bottom 25%
```

**Use case:** Statistical distribution, histogram bins, data skew analysis.

### 2.3 LAG / LEAD

Access values from previous/next rows.

```sql
SELECT
  sale_date,
  revenue,
  LAG(revenue, 1)  OVER (ORDER BY sale_date) AS prev_day,
  LEAD(revenue, 1) OVER (ORDER BY sale_date) AS next_day,
  revenue - LAG(revenue, 1) OVER (ORDER BY sale_date) AS day_over_day_change
FROM daily_sales;
```

**Variants:**
- `LAG(col, n, default)` — n rows back, default if NULL
- `LEAD(col, n, default)` — n rows forward

**Use cases:** Time-series comparisons, period-over-period analysis, gap detection in sequences.

### 2.4 FIRST_VALUE / LAST_VALUE / NTH_VALUE

```sql
SELECT
  employee_name,
  department,
  salary,
  FIRST_VALUE(employee_name) OVER w AS top_earner,
  LAST_VALUE(employee_name)  OVER (
    PARTITION BY department ORDER BY salary DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS bottom_earner
FROM employees
WINDOW w AS (PARTITION BY department ORDER BY salary DESC);
```

**Trap:** `LAST_VALUE` default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — so it returns the same row's value! You must specify `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to get the actual last value.

---

## 3. Aggregate Window Functions

```sql
SELECT
  employee_name,
  department,
  salary,
  SUM(salary)   OVER w AS dept_total,
  AVG(salary)   OVER w AS dept_avg,
  COUNT(*)      OVER w AS dept_size,
  MAX(salary)   OVER w AS dept_max
FROM employees
WINDOW w AS (PARTITION BY department);
```

**Running total:**
```sql
SELECT
  sale_date,
  revenue,
  SUM(revenue) OVER (ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM daily_sales;
```

**Moving average (7-day window):**
```sql
SELECT
  sale_date,
  revenue,
  AVG(revenue) OVER (ORDER BY sale_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM daily_sales;
```

---

## 4. Window Frame Clauses

Frame defines which rows the function operates on within its partition.

| Frame | Meaning |
|-------|---------|
| `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | All rows from start to current |
| `ROWS BETWEEN N PRECEDING AND CURRENT ROW` | Last N rows including current |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | Entire partition |
| `RANGE BETWEEN value PRECEDING AND value FOLLOWING` | Logical range (not row count) |
| `GROUPS BETWEEN N PRECEDING AND N FOLLOWING` | N groups of peer rows |

**Default frames:**
- With `ORDER BY`: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
- Without `ORDER BY`: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`

**ROWS vs RANGE vs GROUPS:**
- `ROWS` — physical rows (deterministic, fast)
- `RANGE` — logical values (rows with same ORDER BY value are peers)
- `GROUPS` — groups of peer rows (PostgreSQL 11+, SQL:2011)

**Performance note:** `ROWS` is always faster — no peer comparison needed. Use `RANGE` only when you truly need logical grouping.

---

## 5. Common Table Expressions (CTEs)

### 5.1 Basic CTE

```sql
WITH active_users AS (
  SELECT id, name
  FROM users
  WHERE last_login > CURRENT_DATE - INTERVAL '30 days'
),
user_orders AS (
  SELECT user_id, COUNT(*) AS order_count, SUM(total) AS total_spent
  FROM orders
  WHERE user_id IN (SELECT id FROM active_users)
  GROUP BY user_id
)
SELECT u.name, uo.order_count, uo.total_spent
FROM active_users u
JOIN user_orders uo ON u.id = uo.user_id;
```

### 5.2 Recursive CTE

**Use case:** Hierarchical data, graph traversal, generating sequences.

```sql
WITH RECURSIVE org_chart AS (
  -- Base case: top-level manager
  SELECT id, name, manager_id, 1 AS depth
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive step: direct reports
  SELECT e.id, e.name, e.manager_id, oc.depth + 1
  FROM employees e
  JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY depth, name;
```

**Graph traversal (find all reachable nodes):**
```sql
WITH RECURSIVE reachable AS (
  SELECT target_node FROM edges WHERE source_node = 'A'

  UNION ALL

  SELECT e.target_node
  FROM edges e
  JOIN reachable r ON e.source_node = r.target_node
)
SELECT DISTINCT * FROM reachable;
```

**Cycle detection:**
```sql
WITH RECURSIVE reachable AS (
  SELECT target_node, ARRAY[source_node, target_node] AS path
  FROM edges WHERE source_node = 'A'

  UNION ALL

  SELECT e.target_node, r.path || e.target_node
  FROM edges e
  JOIN reachable r ON e.source_node = r.target_node
  WHERE NOT e.target_node = ANY(r.path)  -- prevent cycle
)
SELECT DISTINCT target_node FROM reachable;
```

### 5.3 CTE vs Subquery

| Feature | CTE | Subquery |
|---------|-----|----------|
| Readability | High (named, modular) | Low (nested, hard to follow) |
| Reusability | Can reference earlier CTEs | Must repeat |
| Recursive | Yes (WITH RECURSIVE) | No |
| Optimization | Some DBs optimize; others materialize | Usually inlined |
| Scope | One statement | Any expression position |

**MySQL limitation:** CTEs before MySQL 8.0 are non-recursive only. For recursive in MySQL < 8, use session variables or temp tables.

---

## 6. PIVOT and UNPIVOT

### 6.1 PIVOT (Rows → Columns)

Not native in MySQL/PostgreSQL — emulate with CASE + GROUP BY:

```sql
-- Sales per product per quarter
SELECT
  product,
  SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1,
  SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2,
  SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS q3,
  SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS q4
FROM sales
GROUP BY product;
```

**PostgreSQL native (9.4+):**
```sql
SELECT *
FROM crosstab(
  'SELECT product, quarter, revenue FROM sales ORDER BY 1, 2',
  'SELECT DISTINCT quarter FROM sales ORDER BY 1'
) AS ct(product TEXT, q1 NUMERIC, q2 NUMERIC, q3 NUMERIC, q4 NUMERIC);
```

### 6.2 UNPIVOT (Columns → Rows)

```sql
-- Wide table to long format
SELECT product, 'Q1' AS quarter, q1 AS revenue FROM sales_pivot
UNION ALL
SELECT product, 'Q2', q2 FROM sales_pivot
UNION ALL
SELECT product, 'Q3', q3 FROM sales_pivot
UNION ALL
SELECT product, 'Q4', q4 FROM sales_pivot;
```

**PostgreSQL (9.4+):**
```sql
SELECT *
FROM unnest(ARRAY['q1','q2','q3','q4']),
     unnest(ARRAY[q1, q2, q3, q4]);
```

---

## 7. Lateral Joins

`LATERAL` = "for each row of the outer query, run this subquery." Like a correlated subquery but cleaner.

```sql
-- Top 3 orders per customer
SELECT c.name, top_orders.*
FROM customers c
JOIN LATERAL (
  SELECT order_id, total, order_date
  FROM orders o
  WHERE o.customer_id = c.id
  ORDER BY total DESC
  LIMIT 3
) top_orders ON true;
```

**PostgreSQL / MySQL 8.0.14+**

**Without LATERAL** you'd need a correlated subquery or window function with a CTE. LATERAL is more efficient because the DB can short-circuit after LIMIT.

---

## 8. GROUPING SETS, CUBE, ROLLUP

Multi-level aggregation in a single query.

```sql
SELECT
  COALESCE(department, '(all depts)') AS department,
  COALESCE(role, '(all roles)') AS role,
  COUNT(*) AS headcount,
  SUM(salary) AS total_salary
FROM employees
GROUP BY GROUPING SETS (
  (department, role),  -- per dept + role
  (department),        -- per dept only
  (role),              -- per role only
  ()                   -- grand total
);
```

**ROLLUP = GROUPING SETS with hierarchical subtotals:**
```sql
GROUP BY ROLLUP (year, month, day)
-- Produces: (year, month, day), (year, month), (year), ()
```

**CUBE = all combinations:**
```sql
GROUP BY CUBE (department, region)
-- Produces: (dept, region), (dept), (region), ()
```

**`GROUPING()` function** — distinguishes NULL from grouping subtotal:
```sql
GROUPING(department)  -- 1 = this row is a subtotal, 0 = real value
```

---

## 9. GROUPS Frame (SQL:2011)

PostgreSQL 11+, not in MySQL or SQL Server yet.

```sql
-- Moving average over groups of peer rows (same ORDER BY value)
SELECT
  sale_date,
  revenue,
  AVG(revenue) OVER (
    ORDER BY revenue
    GROUPS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS peer_moving_avg
FROM sales;
```

**Groups** treats all rows with the same `ORDER BY` value as one unit. More intuitive than `RANGE` when you have repeated values.

---

## 10. INTERSECT, EXCEPT, MINUS

```sql
-- Users who have orders but no refunds
SELECT user_id FROM orders
EXCEPT
SELECT user_id FROM refunds;

-- Users in both tables
SELECT user_id FROM orders
INTERSECT
SELECT user_id FROM refunds;
```

| Operator | Behavior |
|----------|----------|
| `INTERSECT` | Rows in both queries |
| `EXCEPT` / `MINUS` | Rows in first but not second |
| Duplicates | Removed by default (use `ALL` to keep) |

**PostgreSQL / MySQL 8+ support both.** SQL Server uses `EXCEPT` and `INTERSECT`. Oracle uses `MINUS` instead of `EXCEPT`.

---

## 11. Advanced Subquery Patterns

### 11.1 Scalar Subquery in SELECT

```sql
SELECT
  employee_name,
  salary,
  salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

### 11.2 EXISTS Correlated Subquery

```sql
-- Customers who placed at least one order over $1000
SELECT * FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.id AND o.total > 1000
);
```

### 11.3 LATERAL + DISTINCT ON (PostgreSQL)

```sql
-- Latest order per customer (PostgreSQL idiom)
SELECT DISTINCT ON (c.id) c.name, o.*
FROM customers c
JOIN LATERAL (
  SELECT * FROM orders WHERE customer_id = c.id ORDER BY created_at DESC
) o ON true;
```

---

## 12. Conditional Aggregation

Build complex aggregations without subqueries:

```sql
SELECT
  department,
  COUNT(*) AS total_employees,
  COUNT(*) FILTER (WHERE salary > 80000) AS high_earners,
  COUNT(*) FILTER (WHERE hire_date > '2024-01-01') AS new_hires,
  SUM(salary) FILTER (WHERE status = 'active') AS active_salary
FROM employees
GROUP BY department;
```

**`FILTER` clause** — PostgreSQL, SQLite, DuckDB. MySQL/SQL Server use CASE inside SUM/COUNT:
```sql
SUM(CASE WHEN salary > 80000 THEN 1 ELSE 0 END) AS high_earners
```

---

## 13. Interview Q&A

**Q: Difference between WHERE and HAVING?**
A: WHERE filters rows *before* GROUP BY. HAVING filters groups *after* GROUP BY. You can't use aggregate functions in WHERE (they don't exist yet at that stage).

**Q: How to find the second-highest salary per department?**
A:
```sql
SELECT * FROM (
  SELECT *, DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
  FROM employees
) ranked WHERE rnk = 2;
```

**Q: Running total vs moving average — what frames?**
A: Running total = `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Moving average (7 days) = `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`. Both use `ROWS` for deterministic, performant results.

**Q: When to use CTE vs subquery vs temp table?**
A: CTE for readability and reuse within one query (some DBs materialize automatically). Subquery for one-off expressions. Temp table when you need to reference results multiple times across statements or when the intermediate result is large (avoids re-computation).

**Q: Recursive CTE vs closure table for hierarchies?**
A: Recursive CTE = query-time traversal (flexible, no storage overhead, but slow for deep trees). Closure table = pre-computed pairs (fast reads, write overhead for inserts). Use recursive CTE for ad-hoc queries; closure table for frequent hierarchy queries at scale.

**Q: Can window functions be in WHERE?**
A: No. Window functions execute after WHERE. Use a subquery/CTE to compute the window function, then filter in the outer query:
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (...) AS rn FROM t
) sub WHERE rn = 1;
```

**Q: GROUPING SETS vs multiple GROUP BY UNION ALL?**
A: GROUPING SETS is cleaner, more readable, and usually more efficient (single scan). UNION ALL requires separate scans per grouping level.

---

## Key Takeaways

1. **Window functions** = computation over related rows without collapsing. Master `PARTITION BY` + `ORDER BY` + frame.
2. **ROW_NUMBER vs RANK vs DENSE_RANK** — know the difference for ties and gaps.
3. **LAG/LEAD** — time-series analysis essential. Always specify a default for edge rows.
4. **Frame clause** — default frame traps are common. `ROWS` is always safer and faster than `RANGE`.
5. **CTEs** improve readability; recursive CTEs unlock hierarchical/graph queries.
6. **GROUPING SETS / ROLLUP / CUBE** — multi-level aggregation in one scan.
7. **LATERAL joins** = per-row subqueries with short-circuit. Use when you need TOP-N per group efficiently.
8. **Conditional aggregation** (FILTER or CASE) avoids subqueries for complex counts/sums.
