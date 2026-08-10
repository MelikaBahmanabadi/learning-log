# Chapter 6 — Distributed Databases

**Sources:** Database Internals (Alex Petrov), Designing Data-Intensive Applications (Martin Kleppmann)

---

## 1. Why Distributed Databases?

Scaling a single node hits hardware limits (RAM, CPU, disk I/O, network). Two scaling approaches:

| Approach | Description | Trade-offs |
|---|---|---|
| **Vertical scaling (scale-up)** | Bigger machine | Simple, but expensive, hard limit, single point of failure |
| **Horizontal scaling (scale-out)** | Add more machines | Commodity hardware, no hard limit, but complex |

**Distributed database** = multiple machines cooperating to store data + serve queries. Core challenges:
- **Partitioning (sharding)** — how to split data across nodes
- **Replication** — how to copy data for availability/durability
- **Consistency** — what guarantees across replicas
- **Consensus** — agreeing on a single value across nodes

---

## 2. Partitioning (Sharding)

### 2.1 Strategies

| Strategy | How it works | Pros | Cons |
|---|---|---|---|
| **Key-range** | Partition by key ranges (e.g., user_id 1-1000 → node A) | Efficient range scans | Hotspots if access skewed |
| **Hash-based** | `hash(key) % N` determines partition | Uniform distribution, simple | No range scans; resharding needs consistent hashing |
| **Directory-based** | Lookup table maps key → partition | Flexible, handles skew | Extra lookup, directory becomes bottleneck |

### 2.2 Rebalancing

- **Fixed partitions** — pre-create many partitions (e.g., 1000), assign to nodes. Move partitions on rebalance.
- **Dynamic splitting** — split partitions when they grow too large (e.g., Cassandra vnodes, Raft groups).
- **Consistent hashing** — minimizes data movement when nodes join/leave (used in Dynamo, Cassandra, Riak). [Dynamo; Cassandra Docs]

### 2.3 Secondary Indexes in Partitioned Systems

| Approach | Description |
|---|---|
| **Local (document-partitioned)** | Index lives in same partition as data. Query must fan out to all partitions. |
| **Global (term-partitioned)** | Index partitioned by indexed term. Single partition can answer query, but writes touch multiple index partitions. |

---

## 3. Replication

### 3.1 Replication Models

| Model | Write path | Read path | Consistency |
|---|---|---|---|
| **Single-leader** | All writes → leader → async/sync replicate to followers | Reads from leader (strong) or followers (stale) | Configurable [DI, Ch. 11] |
| **Multi-leader** | Writes to any leader → async replicate to other leaders | Reads from local leader | Eventual; conflicts possible [DI, Ch. 11; DDIA] |
| **Leaderless (Dynamo-style)** | Write to W nodes, read from R nodes, W+R > N (quorum overlap) | Quorum reads/writes | Tunable; quorum overlap alone does not guarantee linearizability [DI, Ch. 11; Dynamo] |

### 3.2 Replication Lag & Consistency

- **Synchronous** — wait for replica ack before acking client. Stronger durability, higher latency, blocks on replica failure. [DI, Ch. 11]
- **Asynchronous** — leader acks immediately. Lower latency, but replica may lag → stale reads, potential data loss on leader failover. [DI, Ch. 11]

**Read-your-writes consistency** — client sees its own writes. Achieved by:
- Reading from leader
- Waiting for replication to catch up (version vectors)
- Sticky sessions to same replica [DDIA]

### 3.3 Multi-leader Conflicts

**Conflict types:**
- **Last-writer-wins (LWW)** — timestamp-based; simple but loses updates. [DDIA]
- **Vector clocks / version vectors** — track causality; detect concurrent writes. [DDIA]
- **CRDTs** — conflict-free replicated data types (e.g., counters, sets). [DDIA]
- **Application-specific** — custom merge logic. [DDIA]

---

## 4. Consensus & Leader Election

### 4.1 The Problem

Multiple nodes must agree on a single value (leader, configuration, log entry) despite failures, network partitions, clock drift.

### 4.2 Paxos vs Raft

| | Paxos | Raft |
|---|---|---|
| Understandability | Hard | Designed for understandability |
| Roles | Proposer, Acceptor, Learner | Leader, Follower, Candidate |
| Log replication | Multi-decree (complex) | Single-decree + log replication |
| Membership changes | Complex | Joint consensus |

**Raft basics:**
- **Leader election** — randomized timeouts, candidate requests votes. [Raft]
- **Log replication** — leader appends, replicates to majority, commits when majority acks. [Raft]
- **Safety** — election restriction (candidate must have all committed entries), leader completeness. [Raft]
- **Cluster membership changes** — joint consensus (old + new config overlap). [Raft]

### 4.3 Use in Databases

- **etcd / Consul / ZooKeeper** — coordination, config, leader election. [etcd Docs; Consul Docs; ZooKeeper Docs]
- **CockroachDB / TiKV / YugabyteDB** — distributed SQL on Raft. [CockroachDB Docs; TiKV Docs; YugabyteDB Docs]
- **Kafka (KRaft)** — Kafka distributes topic data using partitions; KRaft provides the metadata consensus mechanism. Kafka does not use Dynamo/Cassandra-style vnodes for data partitioning. [Kafka Docs]

---

## 5. Distributed Transactions

### 5.1 Two-Phase Commit (2PC)

```
Phase 1 (Prepare): Coordinator asks all participants "can you commit?"
                   Participants lock resources, write prepare to log, reply YES/NO
Phase 2 (Commit):  If all YES → coordinator sends COMMIT
                   If any NO → coordinator sends ABORT
                   Participants release locks after committing/aborting
```

**Problems:** blocking (if coordinator fails after prepare), coordinator is SPOF, locks held during prepare. [DI, Ch. 13]

### 5.2 Three-Phase Commit (3PC)

Adds a **Pre-Commit** phase to reduce blocking — but still not partition-tolerant.

### 5.3 Saga Pattern

For long-running business transactions: chain of local transactions with **compensating actions** for rollback. [DDIA]

```
Order Service → Reserve Inventory → Charge Payment → Confirm Shipping
     ↓                ↓                  ↓                 ↓
  (compensate)   (compensate)       (refund)         (cancel)
```

- **Choreography** — event-driven, each service listens and acts
- **Orchestration** — central coordinator tells participants what to do

### 5.4 Percolator / Spanner Approach

- **Percolator (Google)** — distributed transactions on Bigtable using 2PC + MVCC + locks. [DI, Ch. 13]
- **Spanner** — TrueTime (GPS + atomic clocks) for globally consistent timestamps, Paxos for replication, 2PC for cross-shard transactions. [Spanner]

---

## 6. Distributed Query Execution

### 6.1 Query Planning in Distributed SQL

- **Partition pruning** — only scan relevant partitions
- **Pushdown** — push filters, projections, aggregations to storage nodes
- **Distributed joins** — shuffle (repartition) or broadcast small table
- **Partial aggregation** — compute partial results on each node, combine at coordinator

### 6.2 Shuffle vs Broadcast Join

| | Shuffle (repartition) | Broadcast |
|---|---|---|
| When | Both tables large | One table small |
| Network | High (redistribute both) | Low (send small to all) |
| Memory | Lower per node | Needs memory for broadcast table |

---

## 7. Key Systems Overview

| System | Model | Consistency | Partitioning | Notable |
|---|---|---|---|---|
| **Cassandra** | Leaderless (Dynamo-style) | Tunable consistency levels | Hash-based partitioning / vnodes | Wide-column model, CQL |[Cassandra Docs] |
| **CockroachDB** | Raft per range | Strong (serializable) | Key-range (auto-split) | Distributed SQL, Postgres wire [CockroachDB Docs] |
| **TiDB / TiKV** | Raft per Region | TiDB uses Snapshot Isolation (SI) by default; READ COMMITTED is also supported | Key-range / Regions | MySQL-compatible SQL layer; TiKV provides Raft-replicated transactional storage |
| **YugabyteDB** | Raft per tablet | Strong | Hash + range | Postgres compatible [YugabyteDB Docs] |
| **Spanner** | Paxos per shard | External consistency | Key-range + directories | TrueTime, global scale [Spanner Docs] |
| **DynamoDB** | AWS-managed distributed key-value service | Eventual or strong reads depending on operation/configuration | Hash-based partition key | Global tables support multi-Region replication |
| **MongoDB** | Single-leader per shard | Configurable | Hash or range | Document model [MongoDB Docs] |
| **Aurora** | Single-leader (shared storage) | Strong | N/A (storage scaled) | MySQL/Postgres, decoupled storage [Aurora Docs] |

---

## 8. CAP Theorem & PACELC

### 8.1 CAP

During a network partition (P), a distributed system cannot simultaneously guarantee both strong consistency (C) and availability (A) for all operations.

- **CP behavior** — the system favors consistency and may reject, delay, or otherwise make some operations unavailable when the required quorum cannot be reached.
- **AP behavior** — the system favors availability and may continue serving operations during a partition, with weaker or eventual consistency and conflict resolution depending on the system.

CP/AP labels are not absolute properties of an entire product. The observed behavior depends on the specific operation, consistency level, replication protocol, configuration, and failure scenario. For example, Cassandra can be configured with different consistency levels, while DynamoDB provides different consistency modes for different operations and global-table configurations.

### 8.2 PACELC

Extends CAP: **E**lse (no partition), **L**atency vs **C**onsistency.
- **PC/EC** — prefer consistency over latency when there is no partition, depending on the system's protocol and configuration.
- **PA/EL** — prefer availability/latency over stronger consistency when there is no partition, depending on the system's protocol and configuration.

---

## 9. Interview Q&A

**Q: What is consistent hashing and why is it used?**
A: Maps keys and nodes onto a hash ring. Each key assigned to next node clockwise. Adding/removing a node only affects its neighbors — minimizes data movement. Used in Dynamo, Cassandra, Riak. [Dynamo; Cassandra Docs]

**Q: How does Raft leader election work?**
A: Followers wait randomized election timeout (e.g., 150–300ms). If no heartbeat from leader, become candidate, increment term, request votes. Majority vote → leader. Safety: candidate must have log at least as up-to-date as majority (election restriction). [Raft]

**Q: What's the difference between 2PC and Saga?**
A: 2PC is synchronous, blocking, for short DB transactions across shards. Saga is asynchronous, non-blocking, for long-running business processes with compensating actions.

**Q: Why is Spanner's TrueTime special?**
A: GPS + atomic clocks give bounded clock uncertainty (typically <7ms). Allows assigning globally meaningful commit timestamps, enabling external consistency without coordination on every read. [Spanner]

**Q: What is a "split brain" and how does Raft prevent it?**
A: Two nodes think they're leader simultaneously. Raft prevents it by requiring majority vote — at most one can get majority in a given term. [Raft]

**Q: In a leaderless (Dynamo-style) system, what does W+R > N guarantee?**
A: Quorum overlap — when strict read and write quorums are used and W + R > N, every read quorum intersects every write quorum in at least one replica. This overlap alone does not guarantee linearizability. Stronger consistency guarantees depend on the replication protocol, acknowledgement semantics, version ordering and conflict resolution, read/write coordination, and whether sloppy quorums are used. [DI, Ch. 11; Dynamo]

**Q: How do you handle secondary indexes in a sharded database?**
A: Local index = fan out to all shards (scatter-gather). Global index = partition by indexed term, single shard answers but writes touch multiple index partitions.

**Q: What is the trade-off between synchronous and asynchronous replication?**
A: Sync = stronger durability, no data loss on failover, but higher latency and blocks if replica down. Async = lower latency, but replication lag → stale reads, potential data loss.

**Q: What is read amplification in LSM trees and how does it relate to distributed databases?**
A: Multiple SSTables must be checked on read. In distributed LSM (e.g., CockroachDB, TiKV), this compounds with network RPCs — compaction and bloom filters are critical.

---

## Key Takeaways

1. **Partitioning + Replication** are the two fundamental axes of distributed data systems.
2. **Partitioning strategy** determines query patterns (range vs point) and rebalancing cost.
3. **Replication model** (single-leader, multi-leader, leaderless) determines consistency, latency, and conflict handling.
4. **Consensus (Raft/Paxos)** enables safe leader election and log replication — foundation of CP systems.
5. **Distributed transactions** — 2PC for short cross-shard ops, Saga for long business workflows.
6. **CAP theorem** only applies during partitions; PACELC captures the latency/consistency trade-off always.
7. **Modern distributed SQL** (CockroachDB, TiDB, Yugabyte, Spanner) = Raft/Paxos per shard + distributed query engine + SQL layer.
8. **Consistent hashing** minimizes reshuffling on membership changes.

---

## References

### Books

- [DI] Petrov, A. *Database Internals: A Deep Dive into How Distributed Data Systems Work*. O'Reilly Media, 2019. Ch. 11 (Replication and Consistency), Ch. 12 (Anti-Entropy and Dissemination), Ch. 13 (Distributed Transactions), Ch. 14 (Consensus).
- [DDIA] Kleppmann, M. *Designing Data-Intensive Applications*. O'Reilly Media, 2017. Relevant chapters on replication, partitioning, transactions, faults, and consensus.

### Primary Papers

- [Dynamo] DeCandia, G. et al. "Dynamo: Amazon's Highly Available Key-value Store." SOSP, 2007.
- [Raft] Ongaro, D. and Ousterhout, J. "In Search of an Understandable Consensus Algorithm." USENIX ATC, 2014.
- [Spanner] Corbett, J. C. et al. "Spanner: Google's Globally-Distributed Database." OSDI, 2012.

### Official Documentation

- [Cassandra Docs] Apache Cassandra — Architecture and Guarantees.
- [DynamoDB Docs] Amazon Web Services — DynamoDB Read Consistency.
- [CockroachDB Docs] Cockroach Labs — Architecture and Replication.
- [TiDB Docs] PingCAP — Transactions and Isolation Levels.
- [TiKV Docs] PingCAP — Architecture and Raft.
- [YugabyteDB Docs] YugabyteDB — Architecture and Raft Replication.
- [Spanner Docs] Google Cloud — TrueTime and External Consistency.
- [MongoDB Docs] MongoDB — Read Concern and Write Concern.
- [Aurora Docs] AWS — Aurora Storage Architecture.
- [Kafka Docs] Apache Kafka — Design, Partitions, and Replication.
- [etcd Docs] etcd — Architecture and Raft.
- [Consul Docs] HashiCorp — Consul Architecture and Consensus.
- [ZooKeeper Docs] Apache ZooKeeper — Quorums and Coordination.