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

---

## Ch 4 — Window Functions Basics

What is a window function vs GROUP BY? ; Window function computes across rows related to current row WITHOUT collapsing them — each input row keeps its identity. GROUP BY collapses rows into one output row per group.

What are the three parts of a window function syntax? ; FUNCTION(...) OVER (PARTITION BY ... ORDER BY ... frame_clause). Partition defines groups, order defines sorting within group, frame defines which rows from partition to include.

What is the difference between ROW_NUMBER, RANK, and DENSE_RANK? ; ROW_NUMBER assigns unique sequential numbers (ties get arbitrary order, no gaps). RANK gives same rank to ties but leaves gaps (1,1,3,4). DENSE_RANK gives same rank to ties with no gaps (1,1,2,3).

---

## Ch 4 — LAG / LEAD

What do LAG and LEAD do? ; LAG accesses a row before the current row; LEAD accesses a row after. Used for time-series comparisons (day-over-day change), period-over-period analysis.

What happens to LAG/LEAD at the edges of the partition? ; They return NULL (no previous/next row). Use the default parameter: LAG(col, 1, 0) to return 0 instead of NULL.

---

## Ch 4 — FIRST_VALUE / LAST_VALUE / NTH_VALUE

Why does LAST_VALUE often give the wrong answer? ; Default frame is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW — so LAST_VALUE returns the current row's value. Fix: specify ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING.

---

## Ch 4 — Window Frame Clauses

What's the difference between ROWS, RANGE, and GROUPS frames? ; ROWS = physical rows (fast, deterministic). RANGE = logical values — rows with same ORDER BY value are peers (slower, needs peer comparison). GROUPS = groups of peer rows (PostgreSQL 11+, SQL:2011).

What is the default frame with ORDER BY? Without ORDER BY? ; With ORDER BY: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. Without ORDER BY: the entire partition (equivalent to UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING).

---

## Ch 4 — CTEs

What's the difference between a CTE and a subquery? ; CTE is named, reusable across the query, and improves readability. Subquery is inline, must be repeated if needed twice. CTEs can be recursive (WITH RECURSIVE) — subqueries cannot.

When does a recursive CTE cycle — what's the base case and recursive step? ; Base case (non-recursive term) seeds the result. Recursive step joins back to the CTE itself. UNION ALL combines both. Cycle prevention: track visited nodes in an array and check with NOT x = ANY(path).

---

## Ch 4 — PIVOT / UNPIVOT

How do you pivot rows to columns in MySQL/PostgreSQL? ; Use CASE + GROUP BY: SUM(CASE WHEN quarter='Q1' THEN revenue END) AS q1, etc. PostgreSQL also supports crosstab() from the tablefunc extension.

---

## Ch 4 — LATERAL

What is a LATERAL join? ; Runs the subquery for each row of the outer query — like a correlated subquery but cleaner. Useful for TOP-N per group (LIMIT in the lateral subquery). PostgreSQL and MySQL 8.0.14+.

---

## Ch 4 — GROUPING SETS

What's the difference between ROLLUP and CUBE? ; ROLLUP produces hierarchical subtotals: GROUP BY ROLLUP (year, month) → (year,month), (year), (). CUBE produces all combinations: GROUP BY CUBE (a, b) → (a,b), (a), (b), ().

How does GROUPING() help with GROUPING SETS results? ; GROUPING(col) returns 1 when the row is a subtotal (col is NULL because of the grouping, not because it's actually NULL). Distinguishes real NULL values from grouping NULLs.

---

## Ch 4 — Conditional Aggregation

How do you count rows by condition without a subquery? ; Use FILTER clause: COUNT(*) FILTER (WHERE salary > 80000). PostgreSQL, SQLite, DuckDB. MySQL/SQL Server: SUM(CASE WHEN salary > 80000 THEN 1 ELSE 0 END).

---

## Ch 4 — Advanced Patterns

Why can't you use a window function in the WHERE clause? ; Window functions execute after WHERE (logical query order). Compute in a subquery/CTE, then filter outside.

How do you find the second-highest salary per department? ; Use DENSE_RANK() in a subquery: SELECT * FROM (SELECT *, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk FROM employees) ranked WHERE rnk = 2.

What's the difference between WHERE and HAVING? ; WHERE filters rows BEFORE GROUP BY. HAVING filters groups AFTER GROUP BY. Aggregate functions can't go in WHERE — they don't exist yet at that point.

---

## Ch 4 — Query Perf & Edge Cases

Can window functions use indexes? ; ORDER BY in a window can use an index (same as ORDER BY in a regular query). PARTITION BY benefits from an index on the partition column. A composite index on (partition, order) columns can cover the entire window sort.

How does FILTER execute vs CASE-based conditional aggregation? ; FILTER is semantically clearer and in PostgreSQL can enable different execution strategies (partial aggregation). In practice, both produce similar plans — use FILTER for readability, CASE for compatibility.


---

## Ch 5 — Storage Engines & Data Structures

What is a storage engine? ; The layer that manages physical data organization, indexes, transactions, and recovery on disk. Separate from the query/planner layer. Row-oriented for OLTP, column-oriented for OLAP.

Why do column-oriented stores compress better than row-oriented? ; Each column stores one type with high redundancy — run-length, dictionary, and delta encodings apply well. A row mixes types and values, so compression gains are small.

What is a B+tree and why do most DBs use it? ; Balanced multi-way tree where only leaves hold data, internal nodes hold keys, and leaves are linked in a sorted list. Gives shallow trees (height 2-4), and the leaf list makes range scans fast. InnoDB, PostgreSQL, SQLite all use B+trees.

How does a clustered index (InnoDB primary key) work? ; Table rows are physically stored in a B+tree ordered by the primary key. Secondary indexes point to the PK value, so a secondary lookup = 2 traversals. ORDER BY primary key is essentially free.

Why is a monotonic PK better than a random UUID in InnoDB? ; Monotonic keys append at the right edge — no page splits, no fragmentation. Random UUIDs insert into the middle, causing page splits and write amplification.

What is an LSM tree? ; Log-structured merge: append-only writes to an in-memory memtable, flushed as sorted SSTables, merged in the background by compaction. Optimized for write-heavy workloads (RocksDB, Cassandra, HBase). Trade-off: more read/space amplification.

B-tree vs LSM — which for write-heavy, which for read-heavy? ; LSM for write-heavy: append-only, no random in-place updates. B-tree for read-heavy point lookups: lower read amplification, predictable latency. Choose by workload balance.

What is write-ahead logging (WAL) and why needed? ; Every change is appended to a sequential log BEFORE the data file is updated. Makes lazy buffering safe: on crash, replay the log to recover committed transactions. Provides durability without fsync of every page per commit.

What is a checkpoint? ; A point where dirty pages are flushed to the data file and the WAL is truncated. Crash recovery replays only from the last checkpoint, bounding recovery time.

What is the difference between a latch and a lock? ; Latch: protects in-memory physical structures (buffer pool pages, index nodes), held microseconds, one operation, no transaction scope, no deadlock detection. Lock: protects logical data, held until transaction end, queued, supports deadlock detection.

What do STEAL and NO-FORCE mean in recovery? ; STEAL = engine may flush dirty pages of uncommitted transactions early (needs undo log). NO-FORCE = engine doesn't flush all dirty pages at commit (relies on WAL redo). InnoDB and PostgreSQL are STEAL + NO-FORCE.

How does MVCC let readers not block writers? ; Each transaction sees a consistent snapshot by keeping multiple row versions. Readers read old versions; writers create new versions; undo log / row versioning manages cleanup. No reader/writer lock contention.

What is a hash index and its limitation? ; Maps key to file offset in an append-only log (Bitcask design). O(1) point lookups, but no range scans and must fit in memory. Good for key-value point workloads.

---

## Ch 6 — Consistent Hashing

What is consistent hashing and why is it used? ; Maps keys and nodes onto a hash ring. Each key assigned to the next node clockwise. Adding/removing a node only affects its neighbors — minimizes data movement. Used in Dynamo, Cassandra, Riak.

How does a hash ring work in consistent hashing? ; Nodes and keys are placed on a circle (ring) by hashing. A key goes to the first node clockwise from it. Virtual nodes (vnodes) ensure even distribution and smooth rebalancing.

---

## Ch 6 — Partitioning Strategies

What is the difference between key-range and hash-based partitioning? ; Key-range: partitions by sorted key ranges (e.g., 1-1000 → node A). Enables range scans but hotspots. Hash: hash(key) % N determines partition. Uniform but no range scans.

How do you rebalance partitions when adding a node? ; Fixed partitions: pre-create many partitions, move subsets to new node. Dynamic splitting: split partitions when too large. Consistent hashing: only neighbors' data moves.

What is a virtual node (vnode)? ; A physical node owns multiple "tokens" (slots) on the hash ring. Distributes data more evenly, eases rebalancing on node add/remove. Used in Cassandra, Kafka.

---

## Ch 6 — Replication Models

What are the three replication models? ; Single-leader: all writes → leader → replicas (read scale, simple). Multi-leader: writes to any leader → replicated to others (multi-region, conflict-prone). Leaderless (Dynamo): write to W, read from R, W+R>N (highly available, eventual).

What is the difference between synchronous and asynchronous replication? ; Sync: wait for replica ack before ack to client. Stronger durability, higher latency, blocks on replica failure. Async: ack immediately. Lower latency but replica lag → stale reads, potential data loss.

---

## Ch 6 — Consensus (Raft)

How does Raft leader election work? ; Followers wait a randomized election timeout. If no heartbeat from leader, become candidate, increment term, request votes. If majority votes → leader. Random timeouts prevent split votes.

What is the election restriction in Raft? ; A candidate must have a log at least as up-to-date as the majority (last entry's term + index) to win election. Ensures new leader has all committed entries.

How are logs replicated in Raft? ; Leader receives entry → appends to its log → sends AppendEntries RPCs to followers → entry committed when majority append → leader applies to state machine → tells followers to apply via commit index.

---

## Ch 6 — Distributed Transactions

How does Two-Phase Commit (2PC) work? ; Phase 1: coordinator asks participants "can you commit?" → participants lock resources, write prepare to log, reply YES/NO. Phase 2: if all YES → COMMIT to all; if any NO → ABORT to all.

What is the problem with 2PC? ; Blocking: if coordinator fails after prepare, participants block indefinitely. Coordinator is SPOF. Locks held during entire prepare/commit.

What is the Saga pattern? ; A distributed transaction broken into a sequence of local transactions, each with a compensating action for rollback. Orchestration: central coordinator. Choreography: event-driven, no coordinator.

---

## Ch 6 — CAP & PACELC

What does the CAP theorem state? ; In a network partition (P), you must choose between Consistency (C) and Availability (A). You can't have both. Applies only during partitions — normally you can have both.

What is PACELC? ; Extends CAP: Else (no partition), Latency vs Consistency. PC/EC: prioritize consistency (Spanner, CockroachDB). PA/EL: prioritize latency/availability (Cassandra, DynamoDB).

---

## Ch 6 — Vector Clocks

What is a vector clock? ; Tracks causality across nodes by assigning each node a counter. Each version has a vector (e.g., node A's counter, node B's counter). Detects concurrent updates (when neither vector dominates).

How do you detect conflicts with vector clocks? ; If vector clock X has a higher count than Y in at least one node AND Y has a higher count in at least one node → concurrent (conflict). If one dominates all → happens-before.

---

## Ch 6 — Quorum & Read Repair

What is the quorum requirement in Dynamo-style systems? W+R > N guarantees strong consistency. With N=3, W=2, R=2: 2+2=4>3. A read touches 2 nodes; at least 1 saw the latest write.

What is read repair? ; During a read, if replicas disagree, the reader returns the latest version and writes it back to stale replicas. Repairs happen lazily in the background, not synchronously.

---

## Ch 6 — Distributed Query Execution

How do you handle secondary indexes in a sharded database? ; Local index: fan out query to all shards (scatter-gather). Global index: partition index by indexed term; single shard answers but writes touch multiple index partitions.

When do you use broadcast join vs shuffle join? ; Broadcast: one table small enough to fit in memory — send to all nodes. Shuffle: both tables large — redistribute by hash(key). Shuffle = high network I/O, broadcast = low network but memory pressure.
