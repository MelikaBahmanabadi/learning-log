# Chapter 5 — Storage Engines & Data Structures

**Sources:** Database Internals (Alex Petrov)

---

## 1. Why Storage Engines Matter

A **storage engine** is the layer that manages how data is stored, organized, read, and modified on disk. The DBMS separates:
- **Storage engine** — physical data organization, index structures, transactions, recovery
- **Query layer** — parsing, planning, execution (sits on top of the storage engine)

Two fundamental families:
- **OLTP engines** — row-oriented, optimized for single-row lookups & updates by primary key (MySQL InnoDB, PostgreSQL)
- **OLAP engines** — column-oriented, optimized for scanning many rows / aggregating few columns (ClickHouse, Vertica)

---

## 2. Data Layout: Row-Oriented vs Column-Oriented

| | Row-Oriented | Column-Oriented |
|---|---|---|
| Store | Each row contiguous | Each column contiguous |
| Best for | Point lookups, updates, transactions | Range scans, aggregates over few columns |
| Read pattern | Fetch whole row | Fetch only needed columns |
| Compression | Poor (mixed types in row) | Excellent (same type per column, high redundancy) |
| Typical | OLTP | OLAP / analytics |

**Why columnar compresses better:** a column of integers/booleans has high cardinality redundancy → run-length encoding, dictionary encoding, delta encoding all apply. A row mixes types and values, so compression gains are small.

---

## 3. B-Trees — The Dominant OLTP Index

### 3.1 Structure

A B-tree is a balanced, multi-way tree designed for disk I/O:
- **Internal nodes** — hold sorted keys + child pointers
- **Leaf nodes** — hold the actual keys (+ row pointers or the row data)
- Every node holds many keys → **height stays tiny** (typically 2–4 levels for billions of rows)

```
        [ 20 | 40 ]
       /    |      \
   [5|10|15] [25|30] [45|50|60]        ← internal nodes
```

### 3.2 Properties

- **Balanced** — all leaves at the same depth → every lookup is O(log n) node accesses
- **Log-structured on top of random I/O:** one node = one disk page (typically 4–16 KB), so a lookup is `height` page reads
- **Order / branching factor** = max children per node; higher branching factor → shallower tree → fewer I/Os
- **Self-balancing on insert/delete** via node splits and merges

### 3.3 Lookup Cost

```
B-tree lookup   = O(log_B n)  (B = branching factor)
  ~2–4 disk I/Os for billions of rows
  vs  B+tree scans many siblings
```

**B+tree vs B-tree:** in a B+tree, *only leaves hold data*; internal nodes hold only keys. This means:
- More keys per internal node → higher branching factor → shallower tree
- Leaves linked in a list → efficient range scans (`WHERE x BETWEEN a AND b`)
- All modern DBs (InnoDB, PostgreSQL, SQLite) use **B+tree**, not a plain B-tree

### 3.4 InnoDB Clustered Index (primary key index)

- InnoDB stores table rows **physically ordered by the primary key** in a B+tree
- **Secondary indexes** hold the primary key value as their pointer (not a row address)
- Consequence: lookup by secondary index = 2 index traversals (secondary → PK → row)
- `ORDER BY primary_key` is essentially free (already sorted)

**Implication for schema design:** choose the PK carefully — inserts with random UUIDs cause page splits + fragmentation; monotonically increasing keys (auto-increment) append at the right edge.

---

## 4. LSM Trees (Log-Structured Merge)

### 4.1 The Idea

Instead of updating in place (B-tree), **append-only log + in-memory buffer + background merges**:

```
Write path:
  memtable (in RAM, sorted) → flush to SSTable (sorted file) → background compaction merges SSTables

Read path:
  check memtable → then SSTables newest→oldest (with bloom filters to skip)
```

### 4.2 Pros vs Cons

| | B-tree | LSM |
|---|---|---|
| Write amplification | Lower — in-place update | Higher — rewrites on compaction |
| Read amplification | Lower — ~1 lookup | Higher — multiple SSTables to check |
| Random write cost | High (in-place page updates) | Low — append-only |
| Space amplification | Lower | Higher — stale versions until compaction |
| Compaction | No | Background, tunable (size-tiered / leveled) |

**Use LSM when:** write-heavy workloads (analytics ingestion, time-series, logging, queues). Examples: RocksDB, LevelDB, Cassandra, ScyllaDB, HBase, Bigtable.

**Use B-tree when:** read-heavy, low-latency point lookups (most OLTP). Examples: InnoDB, PostgreSQL, SQLite.

### 4.3 Compaction Strategies

- **Size-tiered compaction (STCS):** merge SSTables of similar size; simple, higher space amplification
- **Leveled compaction (LCS):** merge into fixed-size levels; lower space amplification, more write amplification + more predictable reads
- RocksDB defaults to leveled; Cassandra commonly size-tiered

---

## 5. Hash Indexes

- **In-memory hash index:** `key → offset` in an append-only log file (like Redis AOF / Bitcask)
- **Pros:** O(1) point lookups, dead simple
- **Cons:** no range scans, must fit in memory, crash recovery needs the log replayed or a snapshot
- **Append-only log + hash** is the Bitcask design — the log is the truth, the hash map is a cache of `key → file position`

---

## 6. Buffering & Write-Ahead Log (WAL)

### 6.1 Why buffer at all?

Disk writes are slow; grouping many small writes into one large sequential write is far cheaper. The engine keeps a **buffer pool** (cache of pages) and flushes lazily.

### 6.2 WAL — Write-Ahead Log

To stay durable despite lazy flushing, **every change is first appended to a sequential log** (the WAL):

1. Append change to WAL (sequential, fast) — **durability**
2. Apply change in buffer pool (in-memory) — **speed**
3. Later, flush dirty pages to the main data file — **efficiency**

- On crash: replay WAL → no lost committed transactions (the "write-ahead" ordering: log first, data file second)
- PostgreSQL uses WAL; MySQL InnoDB uses the redo log; both follow this principle
- This is why `fsync` of the log happens per commit but the data file flush is deferred

**Why is WAL sequential append fast?** It avoids random I/O — one contiguous append per transaction instead of scattered page updates. `group commit` batches many transactions' log records into one write.

---

## 7. Page, Block & File Management

- **Page** — smallest unit of storage (4 KB typical; InnoDB 16 KB). Every read/write moves whole pages, not rows
- **Page header** stores metadata (checksum, free space, page number)
- **Row overflow** — long values (BLOB/TEXT) may spill to overflow pages, leaving a pointer in the main page
- **Free space map** tracks pages with room for new rows (avoid scanning for a slot)

---

## 8. Recovery & Durability Concepts

- **Durability (D of ACID)** = once a transaction commits, its effects survive crashes
- Achieved via WAL + checkpointing:
  - **Checkpoint** — force dirty pages to disk so recovery doesn't replay the whole log, only from the last checkpoint
  - **Recovery (Aries-style):**
    1. Redo — replay committed transactions forward
    2. Undo — roll back uncommitted transactions (with compensation)
- **STEAL / NO-FORCE policies:**
  - **NO-STEAL** — dirty pages of uncommitted transactions never written early → simpler undo
  - **STEAL** — can flush dirty pages of uncommitted transactions → needs undo log (InnoDB uses undo log for MVCC + rollback)
  - **FORCE** — flush all dirty pages at commit → expensive
  - **NO-FORCE** — defer flush; rely on WAL redo at recovery → what modern engines do

---

## 9. Concurrency at the Storage Layer

- **Latching** — short-lived protection of in-memory structures (buffer pool pages, index nodes) during a single operation. NOT a transaction concept. Guards *physical* consistency.
- **Locking** — long-lived, transaction-scoped, guards *logical* consistency (row/table locks).
- **MVCC (Multiversion Concurrency Control)** — readers don't block writers: each transaction sees a consistent snapshot by keeping multiple row versions (InnoDB undo log, PostgreSQL row versions).
- Latch vs lock is a classic interview distinction:
  - Latch: protects in-memory structures; held for microseconds; no rollback; non-queueing
  - Lock: protects logical data; held until transaction end; queued; supports deadlock detection

---

## 10. Interview Q&A

**Q: What are the two main types of storage engine and when would you use each?**
A: Row-oriented (OLTP — point lookups, transactional updates; e.g. InnoDB, PostgreSQL) and column-oriented (OLAP — scanning many rows, aggregating few columns; e.g. ClickHouse, Vertica). Columnar wins on compression and scan speed; row-oriented wins on point lookups and writes.

**Q: How does a B-tree index make range scans fast?**
A: In a B+tree, data lives only in leaves, and leaves are linked in a sorted list. A range scan walks the leaf list forward after finding the lower bound — no repeated tree traversal.

**Q: Why can't a leading-wildcard LIKE use a B-tree index?**
A: `LIKE '%x'` has no prefix to locate in the sorted key space — the tree can only navigate by exact/prefix key comparisons. `LIKE 'x%'` works because the prefix narrows the search to a contiguous key range.

**Q: Why is a monotonic primary key better than a random UUID in InnoDB?**
A: InnoDB is a clustered B+tree ordered by PK. Monotonic keys append at the right edge — no page splits, no fragmentation. Random UUIDs insert into the middle, causing page splits and write amplification.

**Q: What is write-ahead logging and why is it needed?**
A: Every change is appended to a sequential log *before* the data file is updated. It makes lazy buffering safe: on crash, replay the log to recover committed transactions. Gives durability without forcing an fsync of every page at commit.

**Q: B-tree vs LSM tree — which do you pick for a write-heavy workload?**
A: LSM — append-only writes, no random in-place updates, better write throughput. Cost: higher write/space amplification and more read amplification (multiple SSTables + compaction). B-trees for read-heavy point lookups.

**Q: What's the difference between latching and locking?**
A: Latching protects in-memory physical structures (buffer pool pages, index nodes) for microseconds within one operation, no transaction scope, no deadlock detection. Locking protects logical data for the whole transaction, is queued, and supports deadlock detection.

**Q: What is a checkpoint?**
A: A point where dirty pages are flushed to the data file and the WAL is truncated/recorded, so crash recovery only replays the log from the last checkpoint — bounds recovery time.

**Q: What does "STEAL / NO-FORCE" mean?**
A: STEAL = engine may flush dirty pages of uncommitted transactions early (needs undo). NO-FORCE = engine doesn't flush all dirty pages at commit (relies on WAL redo). InnoDB and PostgreSQL are STEAL + NO-FORCE.

---

## Key Takeaways

1. **Storage engine = disk-side of the DB:** data layout, indexes, transactions, recovery. Separated from the SQL/query layer.
2. **Row vs column orientation** is the first split — OLTP vs OLAP, point lookups vs scans, compression.
3. **B+tree is the OLTP default:** balanced, tiny height, leaves store data, leaf list enables range scans.
4. **Clustered PK** (InnoDB) means PK choice drives physical layout — avoid random inserts.
5. **LSM trees trade read amplification for write throughput** — the write-heavy alternative (RocksDB, Cassandra).
6. **WAL = durability with lazy flushing:** log first, buffer pool, flush later, replay on crash.
7. **Latch vs lock** — physical vs logical, microsecond vs transaction-scoped. Classic interview question.
8. **Recovery = redo + undo** around a checkpoint; modern engines are STEAL + NO-FORCE.
