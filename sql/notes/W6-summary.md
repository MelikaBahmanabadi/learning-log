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
- **Consistent hashing** — minimizes data movement when nodes join/leave (used in Dynamo, Cassandra, Riak).

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
| **Single-leader** | All writes → leader → async/sync replicate to followers | Reads from leader (strong) or followers (stale) | Configurable |
| **Multi-leader** | Writes to any leader → async replicate to other leaders | Reads from local leader | Eventual; conflicts possible |
| **Leaderless (Dynamo-style)** | Write to W nodes, read from R nodes, W+R > N | Quorum reads/writes | Tunable (eventual to strong) |

### 3.2 Replication Lag & Consistency

- **Synchronous** — wait for replica ack before acking client. Stronger durability, higher latency, blocks on replica failure.
- **Asynchronous** — leader acks immediately. Lower latency, but replica may lag → stale reads, potential data loss on leader failover.

**Read-your-writes consistency** — client sees its own writes. Achieved by:
- Reading from leader
- Waiting for replication to catch up (version vectors)
- Sticky sessions to same replica

### 3.3 Multi-leader Conflicts

**Conflict types:**
- **Last-writer-wins (LWW)** — timestamp-based; simple but loses updates
- **Vector clocks / version vectors** — track causality; detect concurrent writes
- **CRDTs** — conflict-free replicated data types (e.g., counters, sets)
- **Application-specific** — custom merge logic

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
- **Leader election** — randomized timeouts, candidate requests votes
- **Log replication** — leader appends, replicates to majority, commits when majority acks
- **Safety** — election restriction (candidate must have all committed entries), leader completeness
- **Cluster membership changes** — joint consensus (old + new config overlap)

### 4.3 Use in Databases

- **etcd / Consul / ZooKeeper** — coordination, config, leader election
- **CockroachDB / TiKV / YugabyteDB** — distributed SQL on Raft
- **Kafka (KRaft)** — metadata on Raft

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

**Problems:** blocking (if coordinator fails after prepare), coordinator is SPOF, locks held during prepare.

### 5.2 Three-Phase Commit (3PC)

Adds a **Pre-Commit** phase to reduce blocking — but still not partition-tolerant.

### 5.3 Saga Pattern

For long-running business transactions: chain of local transactions with **compensating actions** for rollback.

```
Order Service → Reserve Inventory → Charge Payment → Confirm Shipping
     ↓                ↓                  ↓                 ↓
  (compensate)   (compensate)       (refund)         (cancel)
```

- **Choreography** — event-driven, each service listens and acts
- **Orchestration** — central coordinator tells participants what to do

### 5.4 Percolator / Spanner Approach

- **Percolator (Google)** — distributed transactions on Bigtable using 2PC + MVCC + locks
- **Spanner** — TrueTime (GPS + atomic clocks) for globally consistent timestamps, Paxos for replication, 2PC for cross-shard transactions

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
| **Cassandra** | Leaderless (Dynamo) | Tunable (quorum) | Hash (consistent hashing) | AP, wide rows, CQL |
| **CockroachDB** | Raft per range | Strong (serializable) | Key-range (auto-split) | Distributed SQL, Postgres wire |
| **TiDB / TiKV** | Raft per region | Strong (SI/serializable) | Key-range | MySQL compatible |
| **YugabyteDB** | Raft per tablet | Strong | Hash + range | Postgres compatible |
| **Spanner** | Paxos per shard | External consistency | Key-range + directories | TrueTime, global scale |
| **DynamoDB** | Leaderless | Eventual/Strong | Hash | Managed, single-digit ms |
| **MongoDB** | Single-leader per shard | Configurable | Hash or range | Document model |
| **Aurora** | Single-leader (shared storage) | Strong | N/A (storage scaled) | MySQL/Postgres, decoupled storage |

---

## 8. CAP Theorem & PACELC

### 8.1 CAP

In a **network partition (P)**, you must choose between **Consistency (C)** and **Availability (A)**:
- **CP** — reject writes if partition (e.g., ZooKeeper, etcd, CockroachDB)
- **AP** — accept writes, resolve later (e.g., Cassandra, DynamoDB, Riak)

**Crucial:** CAP only applies during a partition. Normally you can have both.

### 8.2 PACELC

Extends CAP: **E**lse (no partition), **L**atency vs **C**onsistency.
- **PC/EC** — prioritize consistency even when no partition (e.g., Spanner, CockroachDB)
- **PA/EL** — prioritize availability/latency (e.g., Cassandra, DynamoDB)

---

## 9. Interview Q&A

**Q: What is consistent hashing and why is it used?**
A: Maps keys and nodes onto a hash ring. Each key assigned to next node clockwise. Adding/removing a node only affects its neighbors — minimizes data movement. Used in Dynamo, Cassandra, Riak.

**Q: How does Raft leader election work?**
A: Followers wait randomized election timeout (e.g., 150–300ms). If no heartbeat from leader, become candidate, increment term, request votes. Majority vote → leader. Safety: candidate must have log at least as up-to-date as majority (election restriction).

**Q: What's the difference between 2PC and Saga?**
A: 2PC is synchronous, blocking, for short DB transactions across shards. Saga is asynchronous, non-blocking, for long-running business processes with compensating actions.

**Q: Why is Spanner's TrueTime special?**
A: GPS + atomic clocks give bounded clock uncertainty (typically <7ms). Allows assigning globally meaningful commit timestamps, enabling external consistency without coordination on every read.

**Q: What is a "split brain" and how does Raft prevent it?**
A: Two nodes think they're leader simultaneously. Raft prevents it by requiring majority vote — at most one can get majority in a given term.

**Q: In a leaderless (Dynamo-style) system, what does W+R > N guarantee?**
A: Strong consistency (linearizable reads). At least one read node has the latest write.

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
