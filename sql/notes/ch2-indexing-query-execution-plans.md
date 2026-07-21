# Chapter 2 — Indexing & Query Execution Plans

**Sources:** SQL Performance Explained (Winand)

---

## 1. What Is an Index?

An **index** is a data structure that speeds up row lookup at the cost of extra storage and slower writes. Without an index, the DB does a **full table scan** — reads every row to find matches. With an index, it jumps directly to matching rows.

**Analogy:** A book's index lets you jump to page 142 instead of reading every page to find "B-tree."

**The fundamental trade-off:**

| Operation | Without Index | With Index |
|-----------|--------------|------------|
| Read (SELECT) | Full scan — slow | Index seek — fast |
| Write (INSERT/UPDATE/DELETE) | Fast (no index to update) | Slower (must update index too) |
| Storage | Minimal | Extra space for each index |

**Interview tip:** Never say "add an index" as a magic fix. Every index slows writes. The question is always *which queries* need optimization and *which columns* are worth indexing.

---

## 2. B-Tree Index (The Default)

Most databases default to a **B-tree** (balanced tree) index. It maintains sorted order and allows:

- **Equality lookup:** `WHERE id = 42` → O(log N)
- **Range scan:** `WHERE price BETWEEN 10 AND 50` → O(log N + K) where K = matching rows
- **ORDER BY optimization:** data is already sorted
- **Prefix matching:** `WHERE name LIKE 'abc%'` can use the index

```
B-tree structure (simplified):

              [50]
            /      \
        [20,30]   [60,80]
       /  |  \    / |  \
    [10] [25] [35] [55] [70] [90]
```

Each node contains keys and pointers. Leaf nodes store the indexed column values + pointers to the actual rows (or primary key in InnoDB).

**When B-tree fails:**

| Pattern | B-tree? | Why |
|---------|---------|-----|
| `WHERE price > 10` | ✅ Yes | Range scan on sorted data |
| `WHERE name = 'Alice'` | ✅ Yes | Equality on sorted data |
| `WHERE price + tax > 100` | ❌ No | Expression on column — index can't help |
| `WHERE name LIKE '%Alice'` | ❌ No | Leading wildcard — must scan all entries |
| `WHERE UPPER(name) = 'ALICE'` | ❌ No | Function on column — unless functional index |

---

## 3. Index Types

### Primary Key Index
- Unique, not null, clustered in InnoDB (MySQL) — data is physically ordered by PK
- Every InnoDB table has exactly one clustered index (the PK by default)
- PostgreSQL has no true clustered index — `CLUSTER` is a one-time reorg, not maintained
- SQL Server clustered index is logically ordered (B-tree), not a flat sequential file

> ⚠️ Dialect note: Clustered indexes work differently per DB. MySQL/InnoDB: PK is always the clustered index, rows stored in B-tree order. SQL Server: one clustered index per table, logically ordered. PostgreSQL: no persistent clustered index — `CLUSTER` is a one-time heap reorder that future writes do not maintain.

### Unique Index
- Enforces uniqueness + speeds up lookups
- Only one NULL allowed per unique column (in most DBs)

### Composite (Multi-Column) Index
- Index on two or more columns: `CREATE INDEX idx ON orders(customer_id, order_date)`
- **Column order matters!** The index can be used for:
  - `customer_id` alone ✅
  - `customer_id + order_date` ✅
  - `order_date` alone ❌ (leftmost prefix rule)

```sql
-- Composite index: (department_id, salary)
-- These queries CAN use the index:
SELECT * FROM employees WHERE department_id = 5;
SELECT * FROM employees WHERE department_id = 5 AND salary > 80000;

-- This CANNOT (skips leftmost column):
SELECT * FROM employees WHERE salary > 80000;
```

**Interview trap:** *"Why doesn't my composite index work?"*
→ Almost always a leftmost prefix violation. The index is like a phone book sorted by last name, then first name. You can look up "Smith, John" efficiently, but not "John" alone.

### Covering Index
- Contains **all columns** needed by the query — the DB never touches the table rows
- The `EXPLAIN` output shows "Using index" (MySQL) or "Index Only Scan" (PostgreSQL)

```sql
-- If you frequently run:
SELECT customer_id, order_date FROM orders WHERE customer_id = 100;

-- This covering index avoids table access entirely:
CREATE INDEX idx_cover ON orders(customer_id, order_date);
```

### Partial / Filtered Index (PostgreSQL, SQL Server)
- Index only rows matching a condition: `CREATE INDEX idx ON orders(status) WHERE status = 'active'`
- Smaller index, faster maintenance — ideal when you mostly query a subset

### Functional / Expression Index
- Index an expression: `CREATE INDEX idx ON users(UPPER(email))`
- Allows `WHERE UPPER(email) = 'ALICE@EXAMPLE.COM'` to use the index
- Supported in PostgreSQL, MySQL 8+, SQL Server

---

## 4. When Indexes DON'T Help

**Interview question:** *"Under what conditions will the optimizer ignore your index?"*

1. **Leading wildcard:** `LIKE '%term'` — B-tree is sorted, can't skip to the middle
2. **Function on indexed column:** `WHERE YEAR(created_at) = 2024` — create a functional index instead
3. **Type mismatch / implicit cast:** `WHERE phone = 5551234` when phone is VARCHAR — the cast prevents index use
4. **High selectivity filter:** `WHERE gender = 'M'` on a table that's 50% male — the optimizer picks a full scan when sequential I/O is cheaper than index lookup + random I/O per matched row. No fixed percentage threshold (depends on buffer cache, storage, table size).
5. **OR across different indexes:** `WHERE a = 1 OR b = 2` — DB may scan both indexes and merge, or just full scan (optimizer decides)
6. **NOT NULL / NOT IN:** `WHERE status != 'deleted'` often matches most rows — full scan wins

**Interview tip:** "The optimizer chooses a full table scan when it's faster than the index." This isn't a bug — it's correct behavior. Check `EXPLAIN` to confirm.

---

## 5. Reading EXPLAIN Output

`EXPLAIN SELECT ...` shows the query plan without running it. Here's how to read it:

### MySQL EXPLAIN Key Columns

| Column | What to look for |
|--------|-----------------|
| **type** | Access type (best → worst): `system` > `const` > `eq_ref` > `ref` > `range` > `index` > `ALL` |
| **possible_keys** | Indexes the optimizer considered |
| **key** | Index actually chosen (NULL = no index used) |
| **key_len** | Bytes used from the index — tells you how many composite columns are used |
| **rows** | Estimated rows to examine |
| **Extra** | Critical info: `Using index` (covering), `Using filesort` (sort not from index), `Using temporary` (temp table created) |

### PostgreSQL EXPLAIN Output

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 100;
-- Output:
-- Index Scan using idx_customer on orders
--   Index Cond: (customer_id = 100)
--   Rows Removed by Index Recheck: 0

-- For actual execution stats:
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
```

**Key PostgreSQL plan nodes:**

| Node | Meaning |
|------|---------|
| `Seq Scan` | Full table scan |
| `Index Scan` | Uses index, then fetches row from table |
| `Index Only Scan` | All data from index (covering) — best case |
| `Bitmap Index Scan` + `Bitmap Heap Scan` | Index finds row locations, then fetches in batch (reduces random I/O) |
| `Nested Loop` | For each outer row, look up in inner |
| `Hash Join` | Build hash from one table, probe with other |
| `Sort` | Data must be sorted (not from index) |

### Common EXPLAIN Red Flags

- `Using filesort` (MySQL) / `Sort` node (PG) — ORDER BY not satisfied by index
- `Using temporary` (MySQL) / `HashAggregate` with high cost — GROUP BY or DISTINCT creating temp storage
- `ALL` / `Seq Scan` on large table with selective WHERE — missing index
- `rows` estimate much higher than actual result — stats may be stale (run `ANALYZE`)

---

## 6. Execution Plan Anatomy

When a DB runs a query, it goes through these steps:

```
1. PARSE     — syntax check, build AST
2. OPTIMIZE  — choose plan (index selection, join order, join algorithms)
3. EXECUTE   — run the plan, return results
```

**The optimizer's job:** Find the cheapest plan (not the fastest — cost-based). Cost = estimated I/O + CPU. It uses table statistics (row count, null fraction, distinct values, histogram) to estimate costs.

### What the Optimizer Decides

| Decision | Options |
|----------|---------|
| **Access path** | Full scan vs. index scan vs. index-only |
| **Join order** | Which table to start with (drives the plan) |
| **Join algorithm** | Nested loop vs. hash vs. merge |
| **Join type** | inner vs. outer vs. semi-join |
| **Aggregation** | Hash aggregate vs. sort + group |
| **Parallelism** | Which operations to parallelize |

**Interview question:** *"Why would a query be fast in dev but slow in production?"*
→ Different table stats. Dev has 100 rows (full scan is fine). Production has 10M rows (optimizer picks wrong plan because stats are stale or distribution differs). Solution: `ANALYZE` in PostgreSQL, `ANALYZE TABLE` in MySQL, or hint the plan.

---

## 7. Index Maintenance & Anti-Patterns

### Over-Indexing
Having too many indexes slows down every write operation. Each INSERT must update every index. Each UPDATE of an indexed column must rebalance the tree.

**Rule of thumb:** If a column isn't in a WHERE, JOIN ON, or ORDER BY, don't index it.

### Unused Indexes
Find and remove them:

```sql
-- MySQL: check for indexes that are never used
SELECT * FROM sys.schema_unused_indexes;

-- PostgreSQL: check index usage stats
SELECT schemaname, relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- never used
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Index Fragmentation
Over time, B-tree pages become fragmented (deleted rows leave gaps). Solutions:
- MySQL: `OPTIMIZE TABLE` or `ALTER TABLE ... ENGINE=InnoDB`
- PostgreSQL: `REINDEX INDEX` or `VACUUM FULL`
- Generally not worth doing proactively — only when queries are measurably slower

### Implicit Types Prevent Index Use
```sql
-- BAD: implicit cast prevents index
WHERE phone = 5551234       -- phone is VARCHAR, comparing to INT
WHERE created_at LIKE '2024%' -- created_at is DATE, implicit cast to string

-- GOOD: explicit types
WHERE phone = '5551234'
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
```

---

## 8. Composite Index Design Strategies

### The "Equality First, Range Last" Rule

For a composite index `(a, b, c)`:
- Equality on `a` ✅
- Equality on `a, b` ✅
- Range on `a` then equality on `b` ❌ (range stops the index scan)

```sql
-- Index: (status, created_at)
-- GOOD: equality on status, range on created_at
WHERE status = 'active' AND created_at > '2024-01-01'

-- BAD: range on status, equality on created_at
WHERE status IN ('active', 'pending') AND created_at = '2024-06-15'
-- The IN creates a range — index stops at status, can't use created_at
```

### Sort Order in Index

```sql
-- If you frequently query:
SELECT * FROM orders
WHERE customer_id = 100
ORDER BY order_date DESC;

-- This index satisfies both the WHERE and ORDER BY:
CREATE INDEX idx ON orders(customer_id, order_date DESC);
-- Without this, the DB must do an extra sort (Using filesort)
```

### Index for Covering

```sql
-- Frequent query:
SELECT order_date, total FROM orders WHERE customer_id = 100;

-- Covering index (avoids table lookup entirely):
CREATE INDEX idx_cover ON orders(customer_id, order_date, total);
-- The index itself contains all needed data
```

---

## 9. Statistics & Plan Stability

The optimizer relies on **table statistics** to make decisions. Stale stats = bad plans.

```sql
-- PostgreSQL: update stats
ANALYZE orders;

-- MySQL: update stats
ANALYZE TABLE orders;

-- Check when stats were last updated (PostgreSQL)
SELECT relname, last_analyze, last_autoanalyze
FROM pg_stat_user_tables
WHERE relname = 'orders';
```

### Plan Cache & Parameter Sniffing

Databases cache execution plans. With parameterized queries, the first parameters seen determine the plan. If later parameters have very different distributions, the cached plan may be suboptimal.

**Symptoms:** Query is fast for some values, slow for others — same query text, different parameter.

**Solutions:**
- PostgreSQL: `pg_hint_plan` extension or `plan_cache_mode = force_custom_plan`
- SQL Server: `OPTION (RECOMPILE)` or `OPTIMIZE FOR` hint
- General: Use `EXPLAIN ANALYZE` with the specific parameters to see the actual plan

---

## 10. Interview Q&A

**Q: What's the difference between a clustered and non-clustered index?**
A: A **clustered index** controls data row ordering — in MySQL/InnoDB and SQL Server, one per table (usually PK). PostgreSQL has no persistent clustered index: `CLUSTER` reorders the heap once but doesn't maintain it. A **non-clustered index** is a separate structure with row pointers — lookup needs an extra table fetch unless it's a covering index.

**Q: Why would you use a composite index instead of two single-column indexes?**
A: 1) A composite index can satisfy queries that filter on multiple columns simultaneously — two separate indexes require merging. 2) A composite index can serve as a covering index. 3) Fewer indexes = fewer write overhead. Rule: composite when columns are often queried together, single when queried independently.

**Q: Explain the "leftmost prefix" rule.**
A: A composite index `(a, b, c)` can be used for queries on `a`, `a+b`, or `a+b+c` — but NOT for `b`, `c`, or `b+c` alone. The index is sorted by `a` first, then `b` within `a`, then `c` within `b`. Skipping `a` means there's no sorted order to exploit.

**Q: When would the optimizer ignore your index?**
A: Leading wildcard `LIKE '%x'`, function on column, implicit type cast, when the optimizer estimates index lookups + random I/O costs more than a sequential full scan (depends on table size, cache hit rate, storage type — measure with `EXPLAIN ANALYZE`), or stale statistics. Also when OR spans different indexed columns without a UNION rewrite.

**Q: How do you read EXPLAIN output? (MySQL)**
A: Check `type` (access path — `ALL` = full scan, `ref`/`range` = index used), `key` (which index), `rows` (estimated work), and `Extra` (`Using index` = covering, `Using filesort`/`Using temporary` = potential optimization targets).

**Q: What is a covering index and why does it matter?**
A: An index that contains all columns the query needs. The DB serves the query entirely from the index without touching table rows — dramatically reducing I/O. In EXPLAIN, it shows as "Using index" (MySQL) or "Index Only Scan" (PG).

**Q: A query is slow in production but fast in dev. What do you check?**
A: 1) `EXPLAIN` in both environments — different plans? 2) Table stats — `ANALYZE` in production. 3) Data distribution — dev has 100 rows (full scan wins), prod has 10M rows. 4) Index exists in prod? 5) Lock contention or resource pressure. 6) Parameter sniffing — same query, different parameter values.

---

## Key Takeaways

1. B-tree is the default index — handles equality, range, and ORDER BY (if columns are in the right order)
2. Composite index order matters — leftmost prefix rule, put equality columns first, range last
3. A covering index avoids table access entirely — the "Using index" holy grail
4. EXPLAIN is your best friend — check access type, rows estimate, and Extra for red flags
5. Indexes speed reads but slow writes — don't over-index; remove unused ones
6. Stale stats cause bad plans — run ANALYZE when a query suddenly gets slow
