# Flashcards

<!-- Cards in Anki format: Question? ; Answer -->

---

## Ch 1 — SQL Execution Order

In what order is a SQL query logically executed? ; FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT. SELECT is evaluated last!

Why can't you use a SELECT alias in WHERE? ; Because WHERE is evaluated before SELECT. The alias doesn't exist yet. You must repeat the expression or use a subquery/CTE.

---

## Ch 1 — JOIN Types

What's the difference between INNER JOIN, LEFT JOIN, and FULL JOIN? ; INNER = only matching rows | LEFT = all left rows + matches | FULL = all rows from both sides. Unmatched rows get NULLs.

What is a CROSS JOIN and when is it used? ; Cartesian product — every row from A paired with every row from B. E.g., 10 customers × 3 products = 30 rows. Used for generating all combinations like scheduling.

What is a SELF JOIN? Give an example. ; Joining a table to itself. E.g., finding an employee and their manager: SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id.

---

## Ch 1 — Join Algorithms

When is a Nested Loop Join the best choice? ; When the outer input is small and there's an index on the inner table. Each outer row is looked up via index. Cost: O(N × log M).

How does a Hash Join work? ; 1) Build a hash table from the smaller table on the join key, 2) probe it with each row from the larger table. Cost: O(N + M). Best for two large tables with no useful index.

When is a Merge Join used? ; When both inputs are already sorted (e.g., from an index). Both streams are traversed in parallel. Cost: O(N + M) if pre-sorted.

---

## Ch 1 — Correlated Subquery vs JOIN

What is a Correlated Subquery? ; A subquery that references the outer query — executes once per row. Usually slow unless there's an index on the filter column.

What's the difference between EXISTS and IN? ; EXISTS short-circuits on first match and is NULL-safe — critical for NOT EXISTS vs NOT IN. IN materializes the subquery result; with NULLs in the list, NOT IN silently returns nothing. For positive IN vs EXISTS, modern optimizers often produce equivalent plans — use EXPLAIN to confirm. Prefer NOT EXISTS over NOT IN on nullable columns.

Why does `NOT IN (1, 2, NULL)` never return anything? ; Because it's equivalent to x!=1 AND x!=2 AND x!=NULL. x!=NULL is always UNKNOWN, so the whole AND becomes UNKNOWN → row is filtered out. Use NOT EXISTS instead.

---

## Ch 1 — NULL Semantics

What does `NULL = NULL` evaluate to? ; UNKNOWN (neither TRUE nor FALSE). So `WHERE col = NULL` never returns any rows. You must use `WHERE col IS NULL`.

What's the difference between COUNT(col) and COUNT(*)? ; COUNT(col) ignores NULL rows. COUNT(*) counts all rows, including NULLs.

What is `NULL * 0`? ; NULL. Any arithmetic operation with NULL yields NULL. Even 0 * NULL is NULL.

---

## Ch 1 — UNION

What's the difference between UNION and UNION ALL? ; UNION combines results and removes duplicates (requires sort/hash). UNION ALL keeps duplicates (faster). Use UNION ALL unless you actually need dedup.

---

## Ch 1 — SET vs BAG

Does SQL work on Sets or Bags? ; Bag (multiset). SQL tables can have duplicate rows, but mathematical relations cannot. SELECT DISTINCT converts a bag to a set.

---

## Ch 1 — Interview Keys

Why is SELECT * bad in production? ; 1) Extra data (bandwidth, memory), 2) App breaks if schema changes, 3) Covering index won't work, 4) Query intent is unclear.

What's the difference between DELETE vs TRUNCATE vs DROP? ; DELETE = remove specific rows (slow, row-level triggers fire, always rollbackable). TRUNCATE = remove all rows fast — row-level triggers don't fire, but PostgreSQL fires statement-level TRUNCATE triggers. DROP = remove table + schema entirely.

---

## Ch 2 — B-Tree Index Fundamentals

What is a B-tree index and what operations does it support? ; A balanced tree structure that keeps data sorted. Supports equality lookup (O(log N)), range scans (O(log N + K)), ORDER BY, and prefix matching (LIKE 'abc%'). It's the default index in most databases.

Why can't a B-tree index help with `WHERE name LIKE '%Alice'`? ; Leading wildcard forces a full scan — the index is sorted, so you can't skip to the middle. Leading wildcards like `LIKE 'Alice%'` CAN use the index.

Why does `WHERE YEAR(created_at) = 2024` not use an index on created_at? ; The function wraps the indexed column — the optimizer can't match it to the index. Fix: use a range `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'`, or create a functional index.

---

## Ch 2 — Composite Index & Leftmost Prefix

What is the leftmost prefix rule for composite indexes? ; A composite index (a, b, c) can be used for queries on `a` alone, `a+b`, or `a+b+c` — but NOT for `b`, `c`, or `b+c` alone. The index is sorted by `a` first, so skipping `a` breaks the sorted order.

Why put equality columns before range columns in a composite index? ; Equality on a column narrows the scan within that level. A range stops the index scan — so columns after the range can't be used. Example: index (status, created_at) works for `WHERE status='active' AND created_at > '2024-01-01'` but NOT the reverse.

What is a covering index? ; An index containing all columns a query needs, so the DB never touches the table rows. Shows as "Using index" (MySQL) or "Index Only Scan" (PG). Dramatically reduces I/O.

---

## Ch 2 — Index Types

What's the difference between a clustered and non-clustered index? ; Clustered index controls data row ordering — in MySQL/InnoDB and SQL Server, one per table (usually PK). PostgreSQL has no persistent clustered index: CLUSTER reorders the heap once but doesn't maintain it. Non-clustered index is a separate structure with row pointers — lookup needs an extra table fetch unless it's a covering index.

When would you use a partial (filtered) index? ; When you mostly query a subset of rows (e.g., `WHERE status = 'active'`). The index only stores matching rows — smaller, faster to maintain. Supported in PostgreSQL and SQL Server.

---

## Ch 2 — Reading EXPLAIN Output

In MySQL EXPLAIN, what does `type` column tell you? ; The access path, best to worst: system > const > eq_ref > ref > range > index > ALL. ALL = full table scan (usually bad on large tables with selective WHERE).

What does "Using filesort" mean in MySQL EXPLAIN? ; The DB must perform an extra sort step because the ORDER BY can't be satisfied by the index. Often a red flag — add an index covering the ORDER BY columns.

What does "Using temporary" mean in MySQL EXPLAIN? ; A temporary table was created during query execution — usually for GROUP BY, DISTINCT, or certain JOIN patterns. Can be expensive on large datasets.

---

## Ch 2 — Execution Plans & Optimizer

What does the query optimizer decide? ; Access path (full scan vs index), join order, join algorithm (nested loop vs hash vs merge), aggregation strategy (hash vs sort), and parallelism. It's cost-based — finds the cheapest plan, not necessarily the fastest.

Why would a query be fast in dev but slow in production? ; 1) Different table stats — dev has 100 rows (full scan fine), prod has 10M. 2) Stale statistics — run ANALYZE. 3) Data distribution differs. 4) Index missing in prod. 5) Parameter sniffing — same query, different parameter values, cached plan is suboptimal.

What is parameter sniffing? ; The DB caches a plan based on the first parameter values it sees. If later parameters have very different distributions, the cached plan may be suboptimal. Fix: RECOMPILE hint, pg_hint_plan, or plan_cache_mode settings.

---

## Ch 2 — Index Maintenance

When is a full table scan actually faster than using an index? ; When the optimizer estimates that sequential I/O (full scan) is cheaper than index lookup + random I/O per matched row. This depends on table size, storage type, buffer cache, and data distribution — there's no fixed percentage. Use EXPLAIN (ANALYZE, BUFFERS) in PostgreSQL or EXPLAIN in MySQL to confirm the optimizer's choice.

Why does `WHERE phone = 5551234` fail to use an index on a VARCHAR column? ; Implicit type cast — comparing VARCHAR to INT converts every row's value, preventing index use. Fix: `WHERE phone = '5551234'` (explicit string literal).

How do you find unused indexes? ; MySQL: `SELECT * FROM sys.schema_unused_indexes`. PostgreSQL: `SELECT indexrelname, idx_scan FROM pg_stat_user_indexes WHERE idx_scan = 0`. Remove them to speed up writes.
