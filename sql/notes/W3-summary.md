# Chapter 3 — SQL Antipatterns & Better Designs

**Sources:** SQL Antipatterns (Bill Karwin)

---

## 1. What Is an Antipattern?

**Antipattern** = a common-but-flawed solution that seems right at first but causes pain later.

Karwin's framework per antipattern:
1. **Symptom** — what you see/hear ("why is this query slow?")
2. **The Antipattern** — the flawed approach
3. **Better Design** — the correct solution
4. **When It's Actually OK** — exceptions where the antipattern is pragmatically acceptable (the "Boat Anchor" card)

---

## 2. Logical Design Antipatterns

### 2.1 Jaywalking — Comma-Separated Lists in a Column

**Symptom:** Storing multiple values in one column: `account_ids = '1,3,5,7'`

**Problem:**
- Can't use foreign keys, no referential integrity
- `WHERE FIND_IN_SET(account_ids, '3')` is slow — no index use
- Updates are string manipulation hell
- What happens when you need to store 100 IDs? Schema change.

**Better Design:** Join table (intersection table).
```sql
CREATE TABLE AccountContacts (
  contact_id BIGINT REFERENCES Contacts(id),
  account_id BIGINT REFERENCES Accounts(id),
  PRIMARY KEY (contact_id, account_id)
);

SELECT * FROM Contacts c
JOIN AccountContacts ac ON c.id = ac.contact_id
WHERE ac.account_id = 3;
```

**When it's OK:** Nowhere. There's always a join table.

**Interview trap:** *"But what if I only store 3 values max and never query them?"* → You're designing for today. The join table costs nothing. The antipattern costs a rewrite when requirements change. Always use the join table.

---

### 2.2 Naive Trees — Adjacency List for Hierarchies

**Symptom:** A table with `parent_id` for tree structures:
```sql
CREATE TABLE Comments (
  id BIGINT PRIMARY KEY,
  parent_id BIGINT REFERENCES Comments(id),
  body TEXT
);
```

**Problem:**
- `parent_id` can't express paths at depth > 2 with a single query
- In standard SQL, you need recursive CTEs (PostgreSQL, SQL Server, MySQL 8+, SQLite) — but not all DBs support them
- Without recursive CTE: you write N queries for N levels, or app-level loops
- Queries like "find all descendants" or "find all ancestors" are painful

**Better Design Options:**

| Technique | How It Works | Best For |
|-----------|-------------|----------|
| **Path Enumeration** | Store path string: `'1/4/6/7'` | Simple ancestry queries |
| **Nested Sets** | `nsleft` / `nsright` using tree traversal numbers | Frequent subtree reads |
| **Closure Table** | Separate table storing all ancestor-descendant pairs | Deep trees, mixed read/write |

**Path Enumeration:**
```sql
CREATE TABLE Comments (
  id BIGINT PRIMARY KEY,
  path VARCHAR(500),  -- '1/', '1/4/', '1/4/6/7/'
  body TEXT
);

-- Find all ancestors of comment 7 (index on path, use LIKE)
SELECT * FROM Comments
WHERE '1/4/6/7/' LIKE path || '%';
-- Problem: path is app-maintained string, no referential integrity
```

**Nested Sets:**
```sql
CREATE TABLE Comments (
  id BIGINT PRIMARY KEY,
  nsleft INTEGER NOT NULL,
  nsright INTEGER NOT NULL
);

-- Find all descendants of node with nsleft=2, nsright=9
SELECT * FROM Comments
WHERE nsleft >= 2 AND nsright <= 9;

-- Inserting a node requires renumbering all siblings to the right
-- Most deprecated in practice — high maintenance cost
```

**Closure Table (Recommended):**
```sql
CREATE TABLE Comments (
  id BIGINT PRIMARY KEY,
  body TEXT
);

CREATE TABLE TreePaths (
  ancestor BIGINT NOT NULL REFERENCES Comments(id),
  descendant BIGINT NOT NULL REFERENCES Comments(id),
  depth INTEGER NOT NULL DEFAULT 0,  -- distance (0 = self)
  PRIMARY KEY (ancestor, descendant)
);

-- Find all descendants of comment 4
SELECT c.* FROM Comments c
JOIN TreePaths tp ON c.id = tp.descendant
WHERE tp.ancestor = 4;

-- Find all ancestors of comment 6
SELECT c.* FROM Comments c
JOIN TreePaths tp ON c.id = tp.ancestor
WHERE tp.descendant = 6;

-- Insert a leaf: add rows for each (ancestor_of_parent, new_node) + (new_node, new_node)
INSERT INTO TreePaths (ancestor, descendant, depth)
SELECT ancestor, 8, depth + 1 FROM TreePaths WHERE descendant = 7
UNION ALL SELECT 8, 8, 0;

-- Delete a subtree: use ON DELETE CASCADE or manual delete
DELETE FROM TreePaths WHERE descendant = 6;
```

**When adjacency list is OK:** When you only ever query the immediate parent (e.g., an employee's manager) and never need full tree traversal. Shallow hierarchies only.

**Interview tip:** *"How would you model a threaded comments system with infinite nesting?"* → Start with closure table. For very deep trees where write volume is high, consider hybrid: adjacency list for DML + closure table for queries (maintain both).

---

### 2.3 ID Required — Surrogate Key Everywhere

**Antipattern:** Every table gets an auto-increment `id` column, even when a natural key exists.

```sql
CREATE TABLE Bugs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  bug_key VARCHAR(10) NOT NULL UNIQUE,  -- natural key like 'BUG-1234'
  -- id is redundant — bug_key is the real identifier
);
```

**Problems:**
- Adds unnecessary index overhead (PK + unique on natural key)
- Natural keys enforce real business constraints — surrogate keys don't
- JOINs using meaningless integers obscure intent
- Auto-increment IDs can expose business info (competitor knows your order count)

**Better Design:** Use natural keys when they exist and are stable + unique.

```sql
CREATE TABLE Bugs (
  bug_key VARCHAR(10) PRIMARY KEY,  -- 'BUG-1234'
  ...
);
-- Or use UUID for distributed systems
```

**When surrogate keys are good:**
- No stable natural key exists (or the natural key could change — e.g., employee email)
- Natural key is large (> 4 columns, very wide) — a small INT is faster
- Distributed systems (UUID/ULID auto-generated)
- Data warehouse / analytics — natural keys may be wide strings
- Enforced by framework convention (Rails, Django)

**Rule of thumb:** Start with the natural key. Only add a surrogate when the natural key proves problematic (width, mutability, compositeness).

---

### 2.4 Keyless Entry — No Constraints

**Antipattern:** Tables without primary keys, foreign keys, or unique constraints.

**Symptom:** "We enforce data integrity in the application code."

**Problems:**
- Application code has bugs → dirty data
- Every app must re-implement the same checks (mobile, web, API, batch jobs)
- Orphaned rows from DELETE without CASCADE
- Duplicate rows accumulate over time
- The DB can enforce integrity at the write level — atomic, consistent, no race conditions

**Better Design:** Always use declarative constraints.

```sql
CREATE TABLE Orders (
  id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES Customers(id)
    ON DELETE RESTRICT,  -- prevents deleting customers with orders
  order_date DATE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  CONSTRAINT chk_status CHECK (status IN ('pending', 'shipped', 'cancelled'))
);
```

**When skipping constraints is OK:** Prototypes, import scripts (re-add after load), data warehouses (ETL handles integrity upstream), or very high-throughput OLTP where constraint checking is the bottleneck (measure first — rare).

---

### 2.5 Entity-Attribute-Value (EAV)

**Antipattern:** The "generic schema" — one table for all attributes:
```sql
CREATE TABLE Issues (
  issue_id BIGINT PRIMARY KEY
);

CREATE TABLE Attributes (
  issue_id BIGINT REFERENCES Issues(issue_id),
  attr_name VARCHAR(100),    -- 'status', 'priority', 'severity'
  attr_value VARCHAR(255),
  PRIMARY KEY (issue_id, attr_name)
);
```

**Problems:**
- All values stored as VARCHAR — no type safety (date stored as '2024-01-01' or '01/01/24')
- Referential integrity impossible (can't FK to a Users table if value is 'assigned_to')
- `SELECT` becomes a nightmare — you need pivot queries or N self-joins per attribute
- No way to enforce required attributes
- Performance: every attribute is a separate row, so reading "a row" means many joins or GROUP_CONCAT

```sql
-- Getting "a row" requires N joins:
SELECT i.issue_id,
  a1.attr_value AS status,
  a2.attr_value AS priority,
  a3.attr_value AS assigned_to
FROM Issues i
LEFT JOIN Attributes a1 ON i.issue_id = a1.issue_id AND a1.attr_name = 'status'
LEFT JOIN Attributes a2 ON i.issue_id = a2.issue_id AND a2.attr_name = 'priority'
LEFT JOIN Attributes a3 ON i.issue_id = a3.issue_id AND a3.attr_name = 'assigned_to'
WHERE i.issue_id = 1234;
```

**Better Design:** Single Table Inheritance (few shared attributes), Class Table Inheritance (specific tables per subtype), or a document store (JSON/NoSQL) if truly dynamic.

```sql
-- Option 1: Concrete table per subtype
CREATE TABLE Bugs (
  issue_id BIGINT PRIMARY KEY,
  severity VARCHAR(20),
  status VARCHAR(20),
  reported_by BIGINT REFERENCES Users(id)
);

CREATE TABLE FeatureRequests (
  issue_id BIGINT PRIMARY KEY,
  sponsor VARCHAR(100),
  status VARCHAR(20),
  requested_by BIGINT REFERENCES Users(id)
);

-- Option 2: JSONB (PostgreSQL) for truly dynamic attributes
CREATE TABLE Issues (
  issue_id BIGINT PRIMARY KEY,
  issue_type VARCHAR(20) NOT NULL,
  attributes JSONB,
  assigned_to BIGINT REFERENCES Users(id)
);
```

**When EAV is actually OK:**
- Truly dynamic attributes that change per entity type AND per row AND are never queried by value
- Logging / audit trails (attribute name → value pairs as a historical record)
- Product catalog for a small set of highly variable product types (but only if querying by attribute value is rare)

**Interview pass:** EAV is almost always wrong. If you're asked about it in an interview, describe the problems above, then offer the better alternatives. If pressed: "I would only use EAV for audit logs or a sparse, never-queried-against extension point, and I'd push back hard."

---

### 2.6 Polymorphic Associations

**Antipattern:** A foreign key column that can reference *any* table.

```sql
CREATE TABLE Comments (
  comment_id BIGINT PRIMARY KEY,
  parent_type VARCHAR(20),  -- 'Bugs' or 'FeatureRequests'
  parent_id BIGINT,         -- references EITHER Bugs or FeatureRequests
  body TEXT
);
```

**Problems:**
- No foreign key constraint — the DB can't enforce referential integrity
- `parent_id` 123 could reference Bugs or FeatureRequests without any DB-level check
- JOINs require a conditional or UNION:
```sql
SELECT *
FROM Comments c
LEFT JOIN Bugs b ON c.parent_type = 'Bugs' AND c.parent_id = b.id
LEFT JOIN FeatureRequests f ON c.parent_type = 'FeatureRequests' AND c.parent_id = f.id
WHERE c.comment_id = 1;
```
- Adding a new parent type changes all queries

**Better Design:**
1. **Reverse the relationship** — create a separate Comments table per parent type
2. **Or use a shared supertable** (Class Table Inheritance) with a common `Issues` parent table both `Bugs` and `FeatureRequests` reference

```sql
-- Option 1: Separate comments tables per type
CREATE TABLE BugsComments (
  bug_id BIGINT REFERENCES Bugs(id),
  comment_id BIGINT REFERENCES Comments(id) UNIQUE
);

CREATE TABLE FeatureRequestComments (
  feature_id BIGINT REFERENCES FeatureRequests(id),
  comment_id BIGINT REFERENCES Comments(id) UNIQUE
);

-- Query all comments for a bug
SELECT c.* FROM Comments c
JOIN BugsComments bc ON c.id = bc.comment_id
WHERE bc.bug_id = 1234;
```

**When polymorphic associations are OK:** Auditing / logging (no FK enforcement needed — you're recording history, not enforcing integrity). Metadata storage where referential integrity is not required.

---

## 3. Physical Design Antipatterns

### 3.1 Multicolumn Attributes

**Antipattern:** Multiple columns where a related table belongs.

```sql
CREATE TABLE Tags (
  bug_id BIGINT,
  tag1 VARCHAR(50),
  tag2 VARCHAR(50),
  tag3 VARCHAR(50)
);
```

Problems: querying is awkward (`WHERE tag1 = 'x' OR tag2 = 'x' OR tag3 = 'x'`), adding a 4th tag requires ALTER TABLE, nulls waste space.

**Better Design:** A join table (intersection table), just like Jaywalking.

---

### 3.2 Metadata Tribbles

**Antipattern:** Creating separate tables/columns for "similar" data over time.

```sql
CREATE TABLE Bugs_2009 ( ... );
CREATE TABLE Bugs_2010 ( ... );
CREATE TABLE Bugs_2011 ( ... );
-- or columns:
ALTER TABLE Bugs ADD COLUMN tag1 VARCHAR(20);
ALTER TABLE Bugs ADD COLUMN tag2 VARCHAR(20);
ALTER TABLE Bugs ADD COLUMN tag3 VARCHAR(20);
```

**Problems:**
- Querying across years requires UNION ALL on N tables
- Adding a new year/attribute requires schema change
- Maintenance burden grows linearly with time
- No way to enforce global constraints

**Better Design:** A single table with a `year` column — or a partition by year (physical split, logical single table). Use the column for attributes, not the table name.

```sql
-- Logical partitioning (PostgreSQL)
CREATE TABLE Bugs (
  id BIGINT PRIMARY KEY,
  created_at DATE NOT NULL,
  description TEXT
) PARTITION BY RANGE (created_at);

-- Physical partitions per year
CREATE TABLE Bugs_2024 PARTITION OF Bugs
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE Bugs_2025 PARTITION OF Bugs
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

**When it's OK:** Data warehousing with explicit sharding by date range (but use partitioning, not separate tables). Hot/cold data separation in legacy systems — but migrate to partitioning.

---

### 3.3 Rounding Errors — FLOAT for Money

**Antipattern:**
```sql
CREATE TABLE Accounts (
  id BIGINT PRIMARY KEY,
  balance FLOAT  -- WRONG
);
```

**Problem:** Floating point can't represent exact decimal values. `0.1 + 0.2 = 0.30000000000000004`. Losing cents adds up.

```sql
SELECT 0.1 + 0.2;  -- 0.30000000000000004
```

**Better Design:**
```sql
CREATE TABLE Accounts (
  id BIGINT PRIMARY KEY,
  balance DECIMAL(19,4) NOT NULL  -- exact fixed-point
);

-- Or store as cents (BIGINT)
CREATE TABLE Accounts (
  id BIGINT PRIMARY KEY,
  balance_cents BIGINT NOT NULL  -- $100.00 = 10000
);
```

**When FLOAT is OK:** Scientific calculations (measurement uncertainty > precision), aggregate approximations, or when the value is truly approximate anyway.

---

### 3.4 31 Flavors — Enum Column for a Lookup Table

**Antipattern:** `CHECK (status IN ('NEW', 'OPEN', 'FIXED', 'CLOSED'))` or `ENUM` in MySQL when the list should be a lookup table.

```sql
-- MySQL ENUM — can't add 'ARCHIVED' without ALTER TABLE
status ENUM('NEW', 'OPEN', 'FIXED', 'CLOSED')
```

**Problems:**
- ALTER TABLE required to add a new value — locks the table
- No way to store metadata about the status (e.g., "CLOSED → resolved")
- Different tables can't share the same enum (inconsistent lists)
- Referential integrity? Can't FK to an ENUM definition

**Better Design:**
```sql
CREATE TABLE BugStatus (
  status VARCHAR(20) PRIMARY KEY,
  description TEXT,
  is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO BugStatus VALUES
  ('NEW', 'Reported but not triaged'),
  ('OPEN', 'Assigned and being worked on'),
  ('FIXED', 'Resolution committed'),
  ('CLOSED', 'Verified by QA');

ALTER TABLE Bugs
  ADD FOREIGN KEY (status) REFERENCES BugStatus(status);
```

**When ENUM is OK:** The set is truly fixed (ISO country codes? until a new country forms. US state abbreviations? stable since 1959 — HI and AK joined in 1959). But even then, a lookup table costs nothing and gives you more flexibility. When never queried externally — small internal app, status truly never changes.

**Interview tip:** "I prefer lookup tables over ENUMs for anything that could change. ENUMs require DDL, which means a migration and potential downtime. A lookup table is just DML."

---

## 4. Query & Application Antipatterns

### 4.1 Phantom Files — Storing Files Outside the DB

**Antipattern:** Storing only a file path in the DB, the actual file on disk.
```sql
CREATE TABLE Screenshots (
  bug_id BIGINT,
  image_path VARCHAR(200)  -- '/uploads/abc123.png'
);
```

**Problems:**
- DB row and file can get out of sync (DELETE the row, file remains)
- Backup = DB dump + file backup — two separate processes, one fails → data loss
- Filesystem path is fragile (server rename, mount changes)
- Transactional consistency: can't roll back a file write

**Better Design:** Store the file content as BLOB / BYTEA in the DB, OR use an object store (S3) with a UUID reference and keep the backup atomic.

```sql
-- BLOB in DB (small files, < 1 MB)
CREATE TABLE Screenshots (
  bug_id BIGINT NOT NULL,
  screenshot BYTEA,      -- PostgreSQL
  mime_type VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Or object store: keep path + checksum for consistency
CREATE TABLE Screenshots (
  bug_id BIGINT,
  s3_key VARCHAR(200) NOT NULL,
  file_hash VARCHAR(64) NOT NULL,  -- SHA-256 for integrity checks
  mime_type VARCHAR(50),
  CONSTRAINT fk_bug FOREIGN KEY (bug_id) REFERENCES Bugs(id)
);
```

**When storing paths is OK:** Very large files (video, binaries) that don't belong in a DB, or when you have a dedicated file server with its own backup procedure AND the path is stable. But use an object store instead — S3, GCS, or MinIO.

---

### 4.2 Implicit Columns — SELECT * in Views/Procedures

**Antipattern:**
```sql
CREATE VIEW BugView AS SELECT * FROM Bugs;
```

**Problems:**
- `SELECT *` returns columns in whatever order they happen to be in the table definition
- Adding a column to the table → the view returns it too — possibly breaking consuming code
- Renaming a column in the table breaks the view (column might disappear or change name)
- The optimizer can't use covering indexes as effectively with `SELECT *`
- Extra data over the wire

**Better Design:**
```sql
CREATE VIEW BugView AS
SELECT id, bug_key, status, severity, reported_by, assigned_to
FROM Bugs;
```

**When SELECT * is OK:** Ad-hoc queries, quick investigations, never in production code.

---

### 4.3 Passwords — Storing Plaintext

**Antipattern:**
```sql
CREATE TABLE Accounts (
  user_id BIGINT PRIMARY KEY,
  password VARCHAR(100)  -- WRONG — plaintext
);
```

**Better Design:** Never store passwords. Store salted password hashes (bcrypt, scrypt, Argon2). Hash at the application layer before the DB.

```sql
CREATE TABLE Accounts (
  user_id BIGINT PRIMARY KEY,
  password_hash VARCHAR(255) NOT NULL,  -- bcrypt hash
  password_salt VARCHAR(64) NOT NULL    -- unique per user
);
```

**Note:** This is an application-layer responsibility, not a DB-level feature in most databases.

---

### 4.4 Fear of the Unknown — Avoiding NULLs Incorrectly

**Antipattern:** Using empty strings, sentinel values (-1, 'N/A', '1900-01-01') instead of NULL.

```sql
-- Instead of NULL for "not yet assigned"
assigned_to BIGINT NOT NULL DEFAULT -1  -- "no user has ID -1"
-- This breaks:
SELECT * FROM Bugs WHERE assigned_to = -1;  -- returns "unassigned"
-- But what does AVG(assigned_to) return? Nonsense.
```

**Problems:**
- Aggregate functions include sentinel values — `AVG(age)` includes rows where age = -1
- `COUNT(col)` — sentinel values are counted, NULLs aren't
- Every app needs to know the sentinel convention ("-1 means missing")
- Impossible to express "no value" for foreign keys without breaking FK constraints

**Better Design:** Use NULL. It's what the database was designed for. Learn to handle it correctly.

```sql
assigned_to BIGINT REFERENCES Users(id)  -- nullable = NULL means unassigned
```

**When sentinels are OK:** Reporting/BI tools that can't handle NULLs (but fix the tool, not the data), or when NULL is semantically different from "missing" (e.g., NULL = unknown value vs. 0 = known zero cost). But even then, consider a separate flag column.

---

### 4.5 Spaghetti Query Syndrome

**Antipattern:** One giant query that does everything:
- Nested subqueries 5 levels deep
- 12 JOINs in a single statement
- Duplicate logic in multiple subqueries

**Better Design:** Break it down:
1. Use CTEs (WITH clauses) for readability
2. Use temporary tables for intermediate results
3. Use views to encapsulate common subqueries
4. In extreme cases, break into application-level steps

```sql
-- Instead of one 100-line query:
WITH
active_users AS (
  SELECT id FROM Users WHERE last_login > CURRENT_DATE - INTERVAL '30 days'
),
popular_products AS (
  SELECT product_id, COUNT(*) AS cnt
  FROM Orders WHERE user_id IN (SELECT id FROM active_users)
  GROUP BY product_id
  HAVING COUNT(*) > 5
)
SELECT p.*, pp.cnt
FROM Products p
JOIN popular_products pp ON p.id = pp.product_id;
```

---

## 5. Deeper Antipatterns / Synthesis

### 5.1 Index Shotgun

**Antipattern:** Adding indexes without understanding the query patterns, or adding indexes on every column "just in case."

**Better Design:** Profile first. Find the slow queries. Add indexes for specific WHERE/JOIN/ORDER BY patterns. Remove unused indexes. See Ch 2 for details.

### 5.2 Too Many Joins

Closely related to Spaghetti Query — pulling in tables that aren't needed, or using joins instead of pre-aggregated data.

**Smell:** The query has tables that only serve as bridges to get to other tables, deduping via DISTINCT because joins multiply rows.

**Fix:** Use EXISTS for "check if row exists" instead of JOIN, pre-aggregate via CTE.

```sql
-- Instead of:
SELECT DISTINCT c.id, c.name
FROM Customers c
JOIN Orders o ON c.id = o.customer_id
WHERE o.total > 100;

-- Use EXISTS:
SELECT c.id, c.name
FROM Customers c
WHERE EXISTS (
  SELECT 1 FROM Orders o
  WHERE o.customer_id = c.id AND o.total > 100
);
```

### 5.3 Read-Only Code

**Antipattern:** Using SQL like a file format — reading everything, processing in the app, writing back. "The DB is just a bucket."

```sql
-- App reads all rows, sorts in memory, picks top 10
SELECT * FROM Orders;
-- ... app sorts, groups, filters
```

**Better Design:** Push work to the DB (filter, sort, aggregate, paginate). The DB has indexes, caching, and parallel execution. SQL is declarative — tell the DB what you need, not how to compute it.

```sql
SELECT * FROM Orders ORDER BY total DESC LIMIT 10;
```

---

### 5.4 The God Table

**Antipattern:** A table with 50+ columns, used by every feature. "We just add another column."

```sql
CREATE TABLE Users (
  id BIGINT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  -- … 30 more columns including:
  shipping_address TEXT,
  billing_address TEXT,
  preferred_payment VARCHAR(50),
  last_login_ip INET,
  reset_password_token VARCHAR(100),
  reset_password_expires TIMESTAMP,
  profile_picture_url TEXT,
  notification_preferences TEXT,  -- JSON blob
  ...
);
```

**Problems:**
- Every SELECT fetches wide rows even for simple operations (unless carefully scoped)
- Column limits (MySQL has a ~4k column limit, but practical limit is much lower)
- Row size limits (MySQL: 65,535 bytes per row)
- Lock contention — UPDATE on one column locks the whole row
- ORM mapping becomes a nightmare

**Better Design:** Vertical partitioning — split across tables by domain.

```sql
CREATE TABLE Users (id, name, email, created_at);
CREATE TABLE UserAddresses (user_id, type, address_line1, city, ...);
CREATE TABLE UserPreferences (user_id, notification_json, ...);
CREATE TABLE UserSecurity (user_id, password_hash, reset_token, ...);
```

---

## 6. Interview Q&A

**Q: What's the worst SQL antipattern you've seen in production?**
A: (Pick from above + explain the fix concisely. EAV and Jaywalking are the most common, most painful, and easiest to recognize.)

**Q: How would you redesign a system using EAV?**
A: Analyze which attributes are common across all entities (promote to columns), which are subtype-specific (class table inheritance), and which are truly dynamic (JSONB column). Migrate in stages: add new schema, write to both during transition, backfill, drop EAV.

**Q: How do you model hierarchical data in SQL?**
A: Four approaches, each with tradeoffs: adjacency list (simple, limited depth), path enumeration (string-based, good for simple ancestry), nested sets (great for reads, painful writes), closure table (flexible, supports arbitrary depth, recommended for most cases). Choose based on write vs read ratio and max depth.

**Q: When is a surrogate key better than a natural key?**
A: When the natural key is wide, composite (many columns), subject to change, or when you need a uniform key across distributed systems (UUID). Start with natural key if one exists and is stable.

**Q: Why are ENUMs problematic in production?**
A: Adding a value requires DDL (ALTER TABLE → table lock → potential downtime). No referential integrity (can't FK to an ENUM). Different tables drift out of sync. Prefer a lookup table — new values are DML (INSERT), not DDL.

**Q: How would you handle variable attributes for different product types?**
A: Option 1) Single Table Inheritance — one table with nullable columns per subtype. Option 2) Class Table Inheritance — common table + subtype-specific tables. Option 3) JSONB for truly dynamic. Never EAV (entity-attribute-value) — it breaks type safety, referential integrity, and queryability.

**Q: What's wrong with storing comma-separated lists in a column?**
A: Can't use FKs, can't index efficiently, querying requires string functions (FIND_IN_SET, LIKE), updates are string manipulation, no referential integrity. Always use a join table.

**Q: Should money be stored as FLOAT?**
A: Never. Use DECIMAL(precision, scale) or store as cents in an integer column. Floating point rounding errors accumulate and can cause financial discrepancies.

**Q: What's the problem with "we enforce data integrity in the app"?**
A: Every client must re-implement the same logic (mobile, web, API, batch), race conditions exist (two concurrent inserts check → both pass → duplicate), app bugs silently corrupt data. Declarative constraints in the DB are atomic, consistent, and enforced for ALL access paths.

---

## Key Takeaways

1. **Jaywalking** (comma-separated lists) — always use a join table. No exceptions.
2. **EAV** — almost always wrong. Use proper schema design or JSONB.
3. **Naive Trees** — closure table for flexible tree queries; adjacency list only for shallow parent lookups.
4. **Surrogate keys** — not always necessary. Prefer natural keys when stable and present.
5. **FLOAT for money** — never. DECIMAL or integer cents.
6. **ENUMs** — prefer lookup tables. DDL for adding values is expensive.
7. **No constraints** — declarative constraints are better than app-level enforcement.
8. **Metadata Tribbles** — separate tables for time periods = pain. Use partitioning.
9. **SELECT \*** — never in production views/procedures/ORM. Always name columns.
10. **NULL sentinels** — don't use -1 or 'N/A' for "missing." Use NULL, it's what the DB is built for.
