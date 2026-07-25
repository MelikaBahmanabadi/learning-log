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

---

## Ch 3 — Logical Design Antipatterns

What is the "Jaywalking" antipattern? ; Storing multiple values in one column (comma-separated list). Problem: no FK, no index, querying requires FIND_IN_SET or LIKE. Fix: always use a join table.

How do you model hierarchical data in SQL? ; Four techniques: adjacency list (parent_id — simple, depth-limited), nested sets (nsleft/nsright — great reads, painful writes), path enumeration (string path — simple ancestry), closure table (separate ancestor-descendant table — flexible, recommended). Pick closure table for most cases.

What is a Closure Table? ; A separate table storing all ancestor-descendant pairs with depth. Query: find descendants by ancestor, find ancestors by descendant. Insert: copy all ancestors of parent + self. Supports arbitrary depth with single queries.

When is the adjacency list (parent_id) model OK? ; When you only need the immediate parent (e.g., employee → manager) and never need full tree traversal. Shallow hierarchies only.

What's wrong with making every table have an auto-increment id? ; It's the "ID Required" antipattern. Natural keys exist and are stable — use them. Surrogate keys add index overhead, obscure meaning, and expose business info (order count). Start with natural key, add surrogate only when needed.

When are surrogate keys actually good? ; When no stable natural key exists, natural key is wide (>4 columns), or in distributed systems (UUID/ULID). Also for framework convention (Rails, Django).

What's wrong with "we enforce data integrity in the app"? ; The "Keyless Entry" antipattern. App code has bugs → dirty data. Every client re-implements checks. No FK enforcement, orphaned rows. DB constraints are atomic, consistent, and enforced for all access paths.

What is the EAV (Entity-Attribute-Value) antipattern? ; A "generic schema" with rows of (entity_id, attr_name, attr_value). Problems: all values stored as VARCHAR (no type safety), can't enforce FKs, SELECT requires N joins or pivot queries, no required attributes. Almost always wrong.

What are better alternatives to EAV? ; Single Table Inheritance (few shared attributes in one table + nullable subtype columns), Class Table Inheritance (common table + subtype-specific tables), or JSONB for truly dynamic attributes.

What is the Polymorphic Associations antipattern? ; A FK column that references any table: parent_type + parent_id. Problem: no referential integrity (DB can't enforce FK to multiple tables), JOINs need UNION or conditional. Fix: reverse the relationship (separate join table per parent type) or use a shared supertable.

When is Polymorphic Associations OK? ; Auditing/logging where referential integrity isn't needed. Never for domain data.

---

## Ch 3 — Physical Design Antipatterns

What's wrong with storing FLOAT for money? ; Floating point can't represent exact decimals (0.1+0.2=0.30000000000000004). Use DECIMAL(precision, scale) or store as cents in BIGINT.

What is the Metadata Tribbles antipattern? ; Creating separate tables/columns for similar data over time: Bugs_2009, Bugs_2010. Problem: querying across years = UNION ALL N tables, adding a year = schema change. Fix: a single table with a year column + partitioning.

Why are ENUMs problematic in production? ; Adding a value requires ALTER TABLE (DDL → table lock → potential downtime). No referential integrity (can't FK to ENUM). Different tables drift out of sync. Prefer a lookup table — new values are INSERT (DML), not ALTER TABLE.

When are ENUMs acceptable? ; Truly fixed sets (US state abbreviations, ISO country codes — but even then, a lookup table costs nothing). Small internal apps where status never changes and downtime is acceptable.

What's wrong with storing multiple tag columns (tag1, tag2, tag3)? ; Querying is awkward (WHERE tag1='x' OR tag2='x' OR tag3='x'), adding a 4th tag = ALTER TABLE. Fix: join table.

---

## Ch 3 — Query & Application Antipatterns

What's the "Phantom Files" antipattern? ; Storing a file path in the DB, actual file on disk. Problems: DB row & file get out of sync, backup needs two processes, no transactional consistency. Fix: store BLOB in DB (small files) or object store with checksum.

Why is SELECT * bad in views and procedures? ; Returns columns in table-definition order, adding a column changes the view output (breaks consuming code), can't use covering indexes effectively, extra data on wire. Always name columns explicitly.

What's wrong with using -1 or 'N/A' instead of NULL? ; The "Fear of the Unknown" antipattern. Sentinel values break aggregate functions (AVG includes -1, COUNT includes sentinels), every app must know the convention, impossible for FKs. Use NULL — the DB is designed for it.

When are sentinel values OK? ; Reporting tools that can't handle NULLs (but fix the tool, not the data). Or when NULL is semantically different from "missing" (rare — consider a separate flag column).

What's the "Spaghetti Query" antipattern? ; One giant query with 12+ JOINs, 5-level nested subqueries, duplicated logic. Fix: CTEs, temp tables, views, or break into app-level steps.

What's the "God Table" antipattern? ; A table with 50+ columns used by every feature. Problems: wide rows, row/page size limits, lock contention, ORM nightmare. Fix: vertical partitioning — split by domain.

What's the "Too Many Joins" antipattern? ; Pulling in tables only used as bridges, using JOIN where EXISTS suffices, deduping with DISTINCT because JOINs multiplied rows. Fix: use EXISTS for existence checks, pre-aggregate with CTE.

---

## Ch 3 — Interview Keys

What's the worst SQL antipattern and why? ; EAV or Jaywalking — both are common, break normalization, destroy queryability, and require costly rewrites. EAV: all values as VARCHAR, no type safety. Jaywalking: no FK, can't index.

How would you redesign an EAV system? ; Analyze common vs subtype-specific vs dynamic attributes. Common → columns, subtype-specific → class table inheritance, dynamic → JSONB. Migrate in stages: new schema, write to both, backfill, drop EAV.

How would you store a threaded comments system with infinite nesting? ; Closure table. It handles arbitrary depth, ancestor/descendant queries in single SQL, and mixed read/write workloads. Alternative: path enumeration for simpler ancestry-only queries.

Should I use ENUM or a lookup table? ; Always prefer lookup table unless the values are truly fixed forever. ENUM = DDL (ALTER TABLE, lock, downtime). Lookup table = DML (INSERT, no downtime, FK-able).
