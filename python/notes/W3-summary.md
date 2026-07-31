# Ch 3: Dicts, Sets & Mapping Structures

## Books Covered
- **Fluent Python (2nd Ed)** — Ch 3: Dictionaries and Sets, Ch 5: Data Class Builders (namedtuple, typing.NamedTuple intro to mappings)
- **Effective Python (3rd Ed)** — Items 24–26: setdefault, defaultdict, __missing__; Dictionaries and hashing
- **Python Cookbook (3rd Ed)** — Ch 1: Data Structures & Algorithms (defaultdict, Counter, OrderedDict, ChainMap, dedup with sets, calculating with dicts)

## Roadmap Sections Covered
- ✅ Dict: creation, access, methods
- ✅ Dict comprehensions, merging (| operator, Python 3.9+)
- ✅ defaultdict, Counter, OrderedDict, ChainMap
- ✅ `__missing__` hook for custom dict subclasses
- ✅ Set: creation, ops (union, intersection, difference, symmetric diff)
- ✅ Frozenset — hashable set
- ✅ Set comprehensions
- ✅ `UserDict` subclassing vs `dict` subclass
- ✅ `collections.abc.Mapping` & `MutableMapping` abstract base classes
- ✅ Dict view set operations (keys & items as sets)
- ✅ Calculating with dicts (min/max/sorted by value)
- ✅ Order-preserving dedup with `dict.fromkeys()` and set-based generator
- ✅ Hash table internals, hashability rules
- ✅ Membership test time complexities (dict/set = O(1), list = O(n))

---

## 3.1 dict — The Heart of Python

Python's dict is a **hash table** — O(1) average for get/set/delete. In Python 3.7+ dicts preserve **insertion order** (language guarantee, not just CPython).

### Creation

```python
# Literal
d = {"name": "Melika", "age": 25}

# Dict comprehension
squares = {x: x**2 for x in range(5)}

# Constructor
dict(name="Melika", age=25)           # keyword args
dict([("a", 1), ("b", 2)])            # iterable of pairs
dict(zip(["a", "b"], [1, 2]))         # zip two sequences
dict({"a": 1}, b=2)                   # merging literal + kwargs

# Mapping proxy (read-only wrapper)
from types import MappingProxyType
read_only = MappingProxyType({"key": "value"})
read_only["key"]       # "value"
read_only["key"] = "x" # TypeError
```

### Access & Common Methods

```python
d = {"name": "Melika", "age": 25}

# Get
d["name"]              # "Melika" — raises KeyError if missing
d.get("name")          # "Melika"
d.get("country")       # None (no error)
d.get("country", "IR") # "IR" (default)

# Set if missing
d.setdefault("role", "user")  # set "role" = "user" if not present, return value

# Check existence
"name" in d            # True — Pythonic (O(1))

# Delete
del d["age"]
popped = d.pop("name")           # returns value, raises KeyError if missing
popped = d.pop("name", None)     # safe pop with default
last = d.popitem()               # remove & return last inserted (LIFO, Python 3.7+)

# Update
d.update({"x": 1, "y": 2})      # merge in keys

# All keys/values/items — live views (reflect dict changes)
d.keys()
d.values()
d.items()

# Copy
shallow = d.copy()               # shallow copy
same_ref = d.fromkeys(["a", "b"], 0)  # {'a': 0, 'b': 0}
```

### Dict Methods at a Glance

| Method | Description | Returns |
|--------|-------------|---------|
| `d[key]` | Get by key | Value or KeyError |
| `d.get(key, default)` | Safe get | Value or default (None) |
| `d.setdefault(key, default)` | Get or insert default | Value |
| `d[key] = val` | Set | — |
| `d.update(other)` | Merge keys from other | None |
| `d.pop(key, default)` | Remove key | Value or default/KeyError |
| `d.popitem()` | Remove last inserted | (key, value) tuple |
| `del d[key]` | Delete key | — |
| `key in d` | Membership | bool |
| `d.keys()` | All keys | KeysView |
| `d.values()` | All values | ValuesView |
| `d.items()` | All (k, v) pairs | ItemsView |
| `d.clear()` | Remove all | None |
| `d.copy()` | Shallow copy | dict |
| `d \| other` | Merge (Python 3.9+) | new dict |
| `d \|= other` | In-place merge | None |

### Iteration

```python
d = {"a": 1, "b": 2, "c": 3}

for key in d:                    # keys
for key in d.keys():             # explicit keys
for val in d.values():           # values
for key, val in d.items():       # key-value pairs

# Modifying while iterating — copy keys
for key in list(d):
    if condition(key):
        del d[key]
```

### Dict Merging (Python 3.9+)

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

# Merge — new dict (later keys win)
merged = d1 | d2     # {"a": 1, "b": 3, "c": 4}

# In-place merge
d1 |= d2             # d1 becomes {"a": 1, "b": 3, "c": 4}

# Old way (still useful pre-3.9)
merged = {**d1, **d2}
```

### Key Ordering (Python 3.7+)

Dicts **preserve insertion order**. This is a language guarantee.

```python
d = {}
d["z"] = 1
d["a"] = 2
d["m"] = 3
list(d)      # ["z", "a", "m"] — insertion order preserved
list(d.keys())   # ["z", "a", "m"]
list(d.values()) # [1, 2, 3]
list(d.items())  # [("z", 1), ("a", 2), ("m", 3)]
```

### Reversed Iteration (Python 3.8+)

```python
for key in reversed(d):
    print(key)        # "m", "a", "z"
```

---

## 3.2 The `__missing__` Hook

When `d[key]` fails with KeyError, Python calls `__missing__(self, key)` if defined in a **dict subclass**. This lets you handle missing keys dynamically.

```python
class DefaultDict(dict):
    """dict that returns a default for missing keys."""
    def __missing__(self, key):
        return f"unknown:{key}"

d = DefaultDict({"a": 1})
d["a"]          # 1
d["missing"]    # "unknown:missing" — no KeyError!
```

### Real-World: StrKeyDict

```python
class StrKeyDict(dict):
    """dict that stores keys as str, accepts int/str lookup."""
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

d = StrKeyDict({"1": "one", "2": "two"})
d["1"]          # "one"
d[1]            # "one" — converts via __missing__
d["3"]          # KeyError
```

**Gotcha:** `__missing__` is only invoked by `d[key]` — NOT by `d.get(key)` or `key in d`. Override those too if needed.

---

## 3.3 defaultdict

```python
from collections import defaultdict

# Default factory — called for missing keys
dd = defaultdict(list)
dd["a"].append(1)       # {"a": [1]} — list() called automatically
dd["a"].append(2)       # {"a": [1, 2]}
dd["b"].append(3)       # {"b": [3]}

# Common factories
defaultdict(list)       # []
defaultdict(set)        # set()
defaultdict(int)        # 0 (good for counting)
defaultdict(float)      # 0.0
defaultdict(dict)       # {}
defaultdict(lambda: "N/A")  # custom default
```

### Use Cases

```python
# Group items
from collections import defaultdict
names = [("Melika", "Python"), ("Ali", "SQL"), ("Sara", "Python")]
groups = defaultdict(list)
for name, lang in names:
    groups[lang].append(name)
# groups = {"Python": ["Melika", "Sara"], "SQL": ["Ali"]}

# Counting (like Counter)
counts = defaultdict(int)
for word in ["a", "b", "a", "c", "b", "a"]:
    counts[word] += 1
# counts = {"a": 3, "b": 2, "c": 1}
```

**Difference from `dict.setdefault`:** `defaultdict` calls the factory only when needed (lazy). `setdefault` always creates the default value, even if the key exists — wasteful if expensive.

---

## 3.4 collections.Counter

A `Counter` is a dict subclass for counting hashable objects.

```python
from collections import Counter

# Creation
c = Counter(["a", "b", "a", "c", "b", "a"])
# Counter({"a": 3, "b": 2, "c": 1})

c = Counter("abracadabra")
# Counter({"a": 5, "b": 2, "r": 2, "c": 1, "d": 1})

c = Counter(a=3, b=1)     # keyword args
c = Counter({"a": 3, "b": 1})  # dict

# Access & update
c["a"]              # 5 (returns 0 for missing — no KeyError!)
c["z"]              # 0
c["a"] += 1         # increment
c.update("ab")      # add counts
c.update({"a": 2})  # add counts from dict

# Most common
c.most_common(2)    # [("a", 5), ("b", 2)]

# Arithmetic
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2, c=1)
c1 + c2             # {"a": 4, "b": 3, "c": 1} — add counts
c1 - c2             # {"a": 2} — subtract (zero or less = remove)
c1 & c2             # {"a": 1, "b": 1} — intersection (min)
c1 | c2             # {"a": 3, "b": 2, "c": 1} — union (max)

# Iterate
list(c.elements())       # all elements with repeats
# ["a", "a", "a", "a", "a", "b", "b", "c", "d", "r", "r"]
```

---

## 3.5 collections.OrderedDict

Preserves insertion order (like regular dict since Python 3.7), but adds methods.

```python
from collections import OrderedDict

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3

# Move to end/start
od.move_to_end("a")              # move "a" to LAST (default last=True)
od.move_to_end("c", last=False)  # move "c" to FIRST

# Pop operations
od.popitem()                     # remove last (LIFO)
od.popitem(last=False)           # remove FIRST (FIFO)

# Equality comparisons — Order-sensitive
od1 = OrderedDict({"a": 1, "b": 2})
od2 = OrderedDict({"b": 2, "a": 1})
od1 == od2            # False — order matters for OrderedDict
                      # True for regular dict (order-agnostic)
```

**When to use OrderedDict vs dict:**
- Need order-sensitive equality checks → OrderedDict
- Need `move_to_end` → OrderedDict
- Otherwise regular dict is fine (insertion order is guaranteed as of Python 3.7)

---

## 3.6 collections.ChainMap

ChainMap groups multiple dicts into a single view. Lookups search each dict in order.

```python
from collections import ChainMap

defaults = {"theme": "dark", "language": "en"}
user_prefs = {"language": "fa"}
runtime = {"theme": "light"}

# Priority order: runtime > user_prefs > defaults
config = ChainMap(runtime, user_prefs, defaults)

config["theme"]         # "light" — from runtime
config["language"]      # "fa" — from user_prefs
config.get("timeout")   # None — not in any

# Mutations affect the FIRST mapping only
config["new_key"] = "val"  # added to runtime
del config["language"]      # removed from runtime (KeyError if not there)
```

**Use case:** Configuration layering (CLI args → env vars → config file → defaults).

---

## 3.7 UserDict — Easier Dict Subclassing

Subclassing `dict` directly can cause issues — if you override `__setitem__`, methods like `update` and `setdefault` bypass it. `collections.UserDict` wraps an internal `dict` (`self.data`) and routes all operations through your overrides.

```python
from collections import UserDict

class StrKeyDict(UserDict):
    """Keys stored as str, lookup accepts int/str."""
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, value):
        self.data[str(key)] = value

d = StrKeyDict()
d[1] = "one"
d["2"] = "two"
d[1]          # "one"
2 in d        # True (converted to "2")
```

**UserDict vs dict subclass:**
- `UserDict` — safer: `update()`, `setdefault()`, `__init__()` all respect your overrides
- `dict` subclass — lighter but `update` calls `__setitem__` only in Python 3.9+; `__init__` bypassed
- Rule of thumb: use `UserDict` unless you have specific performance reasons for `dict`

### collections.abc Mapping & MutableMapping

```python
from collections.abc import Mapping, MutableMapping

# Mapping: read-only interface (__getitem__, __len__, __iter__, __contains__)
# MutableMapping: read + write (adds __setitem__, __delitem__, pop, update, clear)

class MyMapping(MutableMapping):
    """Implement the protocol — get __iter__, __len__, __getitem__, __setitem__,
       __delitem__ for free: pop, update, clear, keys, values, items."""
    def __init__(self, **kwargs):
        self._data = dict(**kwargs)
    def __getitem__(self, key):
        return self._data[key]
    def __setitem__(self, key, value):
        self._data[key] = value
    def __delitem__(self, key):
        del self._data[key]
    def __iter__(self):
        return iter(self._data)
    def __len__(self):
        return len(self._data)
```

**Why use Mapping/MutableMapping:**
- Inherit tested implementations of `keys()`, `values()`, `items()`, `get()`, `pop()`, `update()`, `clear()`
- Just implement 6 core methods → get 20+ for free
- Use `Mapping` for read-only API, `MutableMapping` for read-write

---

## 3.8 Dict Views as Set-Like

`dict.keys()` and `dict.items()` return **views** that support set operations:

```python
d1 = {"a": 1, "b": 2, "c": 3}
d2 = {"b": 2, "c": 4, "d": 5}

# Keys support full set algebra
d1.keys() & d2.keys()        # {"b", "c"} — intersection
d1.keys() | d2.keys()        # {"a", "b", "c", "d"} — union
d1.keys() - d2.keys()        # {"a"} — difference
d1.keys() ^ d2.keys()        # {"a", "d"} — symmetric diff

# Items also support set ops (items are hashable (key, value) pairs)
d1.items() & d2.items()      # {("b", 2)} — common (key, value) pairs
d1.items() - d2.items()      # {("a", 1), ("c", 3)} — items in d1 not in d2

# Values do NOT support set ops (values may not be hashable)
# d1.values() & d2.values()  # TypeError

# Practical: find keys unique to d1
unique_keys = d1.keys() - d2.keys()

# Find keys added/changed
changed = d1.items() ^ d2.items()
```

**Note:** Set operations on views work because `KeysView` implements the `Set` protocol — it's both a view and a set.

---

## 3.9 Calculating with Dicts

Common patterns for extracting min/max/sorted from dicts:

```python
prices = {"ACME": 45.23, "AAPL": 612.78, "IBM": 205.55, "HPQ": 37.20}

# Min/max by value
min(prices, key=prices.get)       # "HPQ" — key with lowest value
max(prices, key=prices.get)       # "AAPL" — key with highest value

# Get (key, value) pair with min value
min(prices.items(), key=lambda x: x[1])   # ("HPQ", 37.20)

# Sort by value
sorted(prices, key=prices.get)    # ["HPQ", "ACME", "IBM", "AAPL"]
sorted(prices.items(), key=lambda x: x[1])  # sorted (key, value) pairs

# Zip-based approach (works because dicts are ordered 3.7+)
min(zip(prices.values(), prices.keys()))   # (37.20, "HPQ")
```

**Gotcha:** `zip()` stops at the shortest iterable — safe when keys/values match 1:1.

---

## 3.10 Deduplicating with Sets

Remove duplicates from a sequence while preserving order (or not):

```python
# Unordered dedup (loses order)
items = [1, 2, 3, 2, 1, 4, 3, 5]
list(set(items))               # [1, 2, 3, 4, 5] — order not preserved

# Order-preserving dedup (Python 3.7+ dict is ordered)
list(dict.fromkeys(items))     # [1, 2, 3, 4, 5] — order preserved!
# dict.fromkeys creates {1: None, 2: None, ...} — dedup + order

# Generator for generic order-preserving dedup
def dedup(items, key=None):
    seen = set()
    for item in items:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            yield item

list(dedup([1, 2, 3, 2, 1, 4, 3, 5]))   # [1, 2, 3, 4, 5]

# Dedup with key func (e.g. dedup dicts by one field)
data = [{"x": 1}, {"x": 2}, {"x": 1}]
list(dedup(data, key=lambda d: d["x"]))   # [{"x": 1}, {"x": 2}]
```

**Best practice:** Use `set()` for simple dedup when order doesn't matter. Use `dict.fromkeys()` for order-preserving dedup of hashable items. Use the generator pattern for dedup with a key function.

---

## 3.11 Hashing & Hash Tables

### How Dicts Work Internally

Python dict is a **hash table**:

1. `hash(key)` → integer (built-in `hash()` function)
2. Table index = hash & mask (mask = table size - 1)
3. If slot empty → store (key, value) pair
4. If slot occupied → **open addressing**: probe next slot
5. Load factor ≈ 2/3 → resize when exceeded

```python
# Which types are hashable?
hash(42)                # 42 (int → itself)
hash("hello")           # some integer
hash((1, 2, 3))         # works — tuple of hashables
hash([1, 2, 3])         # TypeError — list is unhashable
hash({"a": 1})          # TypeError — dict is unhashable
```

**Hashability rules:**
- An object is hashable if it has a `__hash__()` method that always returns the same value over its lifetime, AND it can be compared for equality (`__eq__()`)
- Mutable objects are **NOT** hashable (list, set, dict)
- Immutable objects often ARE hashable (int, str, tuple — if all elements are hashable)
- User-defined objects are hashable by default (by identity — `id()`)

### Hash Table Trade-offs

| Aspect | dict/set | list |
|--------|----------|------|
| Membership | O(1) average | O(n) |
| Get by key | O(1) | N/A (index) |
| Insert | O(1) average | O(1) append, O(n) insert |
| Memory | More (hash table overhead) | Less |
| Order | Insertion order (3.7+) | Index order |
| Requirements | Keys must be hashable | Any elements |

### Speed Comparison

```python
# O(1) — dict membership
lookup = {"apple": True, "banana": True, "cherry": True}
"banana" in lookup   # O(1) — FAST

# O(n) — list membership
items = ["apple", "banana", "cherry"]
"banana" in items    # O(n) — SLOW for large lists
```

---

## 3.12 Sets & Frozenset

Sets are **unordered collections of unique hashable elements**. Backed by a hash table (same as dict keys).

### Creation

```python
# Literal
s = {1, 2, 3}

# Constructor
s = set([1, 2, 2, 3])       # {1, 2, 3} — dedup
s = set("hello")             # {"h", "e", "l", "o"}
s = set()                    # empty set (not {} — that's empty dict!)
empty_set = set()            # ✅
empty_dict = {}              # ❌ — that's a dict

# Set comprehension
s = {x**2 for x in range(10) if x % 2 == 0}
# {0, 4, 16, 36, 64}
```

### Common Methods

```python
s = {1, 2, 3}

s.add(4)                # {1, 2, 3, 4}
s.remove(4)             # {1, 2, 3} — KeyError if missing
s.discard(99)           # no-op — no error if missing
s.pop()                 # remove & return arbitrary element
s.clear()               # empty set

# Copy
s.copy()                # shallow copy
frozenset(s)            # immutable copy
```

### Set Algebra

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b               # {1, 2, 3, 4, 5, 6}  — union
a & b               # {3, 4}              — intersection
a - b               # {1, 2}              — difference (in a not in b)
a ^ b               # {1, 2, 5, 6}        — symmetric difference

# Methods (accept any iterable)
a.union(b)                # same as a | b
a.intersection(b)         # same as a & b
a.difference(b)           # same as a - b
a.symmetric_difference(b) # same as a ^ b

# In-place update
a |= b                    # a = a | b
a &= b                    # a = a & b
a -= b                    # a = a - b
a ^= b                    # a = a ^ b

# Comparison
a <= b                    # subset? (a is subset of b)
a < b                     # proper subset?
a >= b                    # superset?
a > b                     # proper superset?
a == b                    # equal?
a.isdisjoint(b)           # no common elements?
```

### Frozenset — Immutable Set

```python
fs = frozenset([1, 2, 3])

# Immutable — no add/remove/update
fs.add(4)              # AttributeError
fs |= {4}              # TypeError

# Hashable — can be dict key or set member
d = {fs: "value"}      # ✅ frozenset is hashable
s = {frozenset([1, 2])}  # ✅ set of frozensets

# Useful for nested sets and dict keys
```

**When to use frozenset:**
- As a dict key (sets aren't hashable)
- Inside another set
- When you need an immutable, hashable collection of unique elements
- When you want to prevent mutation

### Set Operations as Predicates

```python
# Check if ALL items in a are in b (subset)
a <= b

# Check if ANY items in common
a & b          # non-empty = overlap
a.isdisjoint(b) # True if no overlap

# Check superset
required = {"python", "sql", "maths"}
skills = {"python", "sql", "maths", "pandas"}
required <= skills   # True — all required skills present
```

---

## 3.13 Dict Internals & Key Order

### Memory Overhead

Dicts use more memory than lists because of the hash table structure:
- Hash table: about 1/3 of slots are empty (load factor ~2/3)
- Each slot stores: hash, key pointer, value pointer
- Key ordering requires extra bookkeeping (Python 3.7+ uses a compact array representation — reduces memory vs old dict)

### Key Mutation Danger

```python
class BadKey:
    def __init__(self, val):
        self.val = val
    def __hash__(self):
        return hash(self.val)
    def __eq__(self, other):
        return self.val == other.val

k = BadKey(10)
d = {k: "value"}
k.val = 20          # MUTATE after insertion
d[k]                # KeyError — hash changed!
k in d              # False — can't find it anymore
```

**Rule:** Never use mutable objects as dict keys. If you must use a custom object, make it immutable.

---

## 3.14 Mapping Comparison

| Feature | dict | defaultdict | OrderedDict | Counter | ChainMap |
|---------|------|-------------|-------------|---------|----------|
| Missing key | KeyError | Factory default | KeyError | Returns 0 | Next mapping |
| Order preserved | ✅ (3.7+) | ✅ | ✅ | ✅ | ✅ |
| Order-sensitive eq | ❌ | ❌ | ✅ | N/A | N/A |
| move_to_end | ❌ | ❌ | ✅ | ❌ | ❌ |
| Counting sugar | ❌ | ❌ | ❌ | ✅ | ❌ |
| Multi-dict view | ❌ | ❌ | ❌ | ❌ | ✅ |
| Memory | High | High | High | High | Low (views) |

---

## 3.15 dict, set & frozenset vs Hash Table Summary

| Collection | Hashable req | Ordered | Mutable | Hashable itself |
|------------|-------------|---------|---------|-----------------|
| `dict` | Keys yes | ✅ (3.7+) | ✅ | ❌ |
| `set` | Elements yes | ❌ | ✅ | ❌ |
| `frozenset` | Elements yes | ❌ | ❌ | ✅ |

---

## 3.16 Practice Checklist

- [ ] Create dicts with literal, comprehension, constructor, zip
- [ ] Use `get`, `setdefault`, `defaultdict` for safe access
- [ ] Count and group items with `Counter` and `defaultdict`
- [ ] Use `|` operator to merge dicts (Python 3.9+)
- [ ] Implement `__missing__` in a dict subclass
- [ ] Subclass dict via `UserDict` vs direct `dict` — know the difference
- [ ] Implement `Mapping`/`MutableMapping` ABC with 6 core methods
- [ ] Use dict view set operations (`keys() &`, `items() ^`)
- [ ] Calculate min/max/sorted over dicts using `key=prices.get`
- [ ] Dedup with `dict.fromkeys()` and a set-based generator
- [ ] Use `ChainMap` for layered configuration
- [ ] Perform set algebra (union, intersection, difference, symmetric diff)
- [ ] Use `frozenset` as dict keys
- [ ] Understand hashability rules and hash table internals
- [ ] Compare dict/set O(1) membership vs list O(n)

---

## Flashcards

See: [flashcards.md](../flashcards.md), [flashcards-fa.md](../flashcards-fa.md)

## Progress

- [ ] Read Fluent Python Ch 3 — Dictionaries and Sets
- [ ] Read Fluent Python Ch 5 — Data Class Builders
- [ ] Practice: defaultdict, Counter, ChainMap, set algebra
- [ ] Practice: UserDict, Mapping ABC, dict view set operations, dedup
- [ ] Implement a dict subclass with __missing__
- [ ] Optimize membership checks: use set/dict instead of list for O(1)
