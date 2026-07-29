# Ch 2: Sequences, Lists, Tuples & Slicing

## Books Covered
- **Fluent Python (2nd Ed)** — Ch 2: An Array of Sequences, Ch 3: Dictionaries and Sets (intro on sequence protocol)
- **Python Cookbook (3rd Ed)** — Ch 1: Data Structures & Algorithms (lists, tuples, slicing, bisect)

## Roadmap Sections Covered
- ✅ Lists: creation, indexing, slicing, methods
- ✅ Tuples: immutable sequences, named tuples
- ✅ Slicing deep dive: `[start:stop:step]`, slice objects, assignment to slices
- ✅ List internals: over-allocation, time complexity
- ✅ Array, Deque, and alternative sequence types
- ✅ `bisect` module for sorted sequences
- ✅ `memoryview` and `struct` for binary data
- ✅ Sequence protocol (`__getitem__`, `__len__`)

---

## 2.1 Sequence Protocol

Python sequences implement at least `__len__` and `__getitem__`. This is the **sequence protocol**.

```python
class MySeq:
    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        # Supports both int and slice
        return self._items[index]

    def __contains__(self, item):
        return item in self._items

seq = MySeq([10, 20, 30, 40])
len(seq)        # 4
seq[1]          # 20
seq[1:3]        # [20, 30]
30 in seq       # True
```

**Key insight:** `__getitem__` that handles slices properly makes your class support slicing, iteration, and `reversed()`.

---

## 2.2 Lists — The Workhorse

### Creation

```python
# Literal
nums = [1, 2, 3]
mixed = [1, "a", 3.14]

# Constructor
list("abc")           # ['a', 'b', 'c']
list(range(5))        # [0, 1, 2, 3, 4]

# Repetition
zeros = [0] * 5       # [0, 0, 0, 0, 0]

# List comprehension
squares = [x**2 for x in range(5)]

# From generator
list(x**2 for x in range(5))
```

### Indexing

```python
nums = [10, 20, 30, 40, 50]

nums[0]       # 10 — first
nums[-1]      # 50 — last
nums[-2]      # 40 — second-to-last
```

### Common Methods

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `append(x)` | Add to end | O(1) amortized |
| `extend(iter)` | Add all items | O(k) where k = len(iter) |
| `insert(i, x)` | Insert at position | O(n) — shifts elements |
| `pop()` | Remove & return last | O(1) |
| `pop(i)` | Remove & return at i | O(n) — shifts elements |
| `remove(x)` | Remove first occurrence | O(n) |
| `index(x)` | Find first index | O(n) |
| `count(x)` | Count occurrences | O(n) |
| `sort()` | In-place sort | O(n log n) |
| `reverse()` | In-place reverse | O(n) |
| `copy()` | Shallow copy | O(n) |
| `clear()` | Remove all | O(n) |

```python
nums = [1, 2, 3, 4, 5]
nums.append(6)           # [1, 2, 3, 4, 5, 6]
nums.extend([7, 8])      # [1, 2, 3, 4, 5, 6, 7, 8]
nums.insert(0, 0)        # [0, 1, 2, ...]
nums.pop()               # 8 — removes last
nums.pop(0)              # 0 — removes first
nums.remove(4)           # removes value 4
nums.sort(reverse=True)  # descending sort
```

### List Internals

**Over-allocation:** When a list grows, CPython allocates extra capacity to make future `append`s cheap.

```python
import sys
nums = []
sizes = []
for i in range(50):
    nums.append(i)
    sizes.append(sys.getsizeof(nums))

# Plot sizes — you see jumps when over-allocation kicks in.
# Growth pattern: 0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
```

**Time complexity rule of thumb:**
- Append/pop from end: O(1) amortized
- Insert/pop from start: O(n) — every element shifts
- Indexing: O(1)
- Contains (`x in list`): O(n) — linear scan

**When to use list vs alternatives:**
| Task | Best choice | Why |
|------|------------|-----|
| Stack (LIFO) | `list` | `append()`/`pop()` at end = O(1) |
| Queue (FIFO) | `collections.deque` | `popleft()` is O(1); `list.pop(0)` is O(n) |
| Homogeneous numeric data | `array.array` | Memory-efficient, type-constrained |
| Thread-safe queue | `queue.Queue` | Built-in synchronization |

---

## 2.3 Slicing Deep Dive

### Basic Slicing

```python
seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

seq[2:5]             # [2, 3, 4] — index 2 up to (not including) 5
seq[:4]              # [0, 1, 2, 3] — from start
seq[6:]              # [6, 7, 8, 9] — to end
seq[:]               # full copy (shallow)
seq[::2]             # [0, 2, 4, 6, 8] — step
seq[::-1]            # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] — reverse
seq[2:8:2]           # [2, 4, 6]
```

### Slice Objects

`seq[start:stop:step]` creates a `slice(start, stop, step)` object and passes it to `__getitem__`.

```python
s = slice(2, 8, 2)
seq[s]               # [2, 4, 6]

# Named slices for readability
FIRST_HALF = slice(None, 5)
seq[FIRST_HALF]      # [0, 1, 2, 3, 4]
```

### Slice Assignment

You can **replace** or **delete** slices in-place (list only — tuples are immutable):

```python
nums = list(range(10))

# Replace slice with iterable
nums[2:5] = [20, 30, 40]     # [0, 1, 20, 30, 40, 5, 6, 7, 8, 9]

# Replace with different length — list shrinks/grows
nums[2:5] = [100]            # [0, 1, 100, 5, 6, 7, 8, 9]
# Here [20, 30, 40] replaced by [100] — list shrinks

nums[2:2] = [50, 60]         # Insert at index 2 — [0, 1, 50, 60, 100, 5, ...]

# Step-slice assignment (length must match!)
nums[::2] = [0, 0, 0, 0, 0]  # Replace every other element

# Delete slice
nums[3:6] = []               # Remove elements [3:6]

del nums[3:6]                # Same effect
```

**Key rule for step-slice assignment:** The assigned iterable must have exactly the same length as the target slice.

### Multi-dimensional Slicing

Python's built-in sequences are 1D, but NumPy uses `tuple`-based indexing for n-dimensions:

```python
# NumPy (not built-in, but convention)
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix[0:2, 1:3]   # → [[2, 3], [5, 6]]

# For custom classes, __getitem__ receives a tuple when indexed like seq[1, 2]
class Matrix:
    def __getitem__(self, key):
        if isinstance(key, tuple):
            row, col = key
            return self._data[row][col]
```

### Ellipsis

`...` (the `Ellipsis` object) is used in NumPy and custom containers for "all remaining dimensions."

```python
# NumPy
arr[..., 0]    # All rows, column 0
arr[0, ...]    # Row 0, all columns
```

---

## 2.4 Tuples — Immutable Sequences

### Creation

```python
empty = ()              # empty tuple
single = (1,)           # trailing comma REQUIRED
point = (3, 4)          # two elements
nested = (1, (2, 3))    # nested tuple

# Without parentheses (tuple packing)
a = 1, 2, 3             # (1, 2, 3)

# Constructor
tuple([1, 2, 3])        # (1, 2, 3)
tuple(range(5))         # (0, 1, 2, 3, 4)
```

### Immutability

Tuples are **immutable** — you can't change elements in-place:

```python
t = (1, 2, 3)
t[0] = 10       # TypeError: 'tuple' object does not support item assignment
t.append(4)     # AttributeError: 'tuple' object has no attribute 'append'
```

But if a tuple contains a mutable object, that object CAN be mutated:

```python
t = (1, [2, 3], 4)
t[1].append(99)   # OK! t is now (1, [2, 3, 99], 4)
```

**Immutability means:** the *references* in the tuple can't change. The objects they point to can be mutated.

### Tuple as Record (Unpacking)

```python
# Unpacking
lat, lon = (35.6895, 51.3890)

# Swapping
a, b = b, a

# Extended unpacking (Python 3+)
first, *middle, last = range(10)
# first=0, middle=[1,2,3,4,5,6,7,8], last=9

# Ignoring values
_, department, _ = ("Melika", "Engineering", "Python")
```

### Tuple vs List — When to Use Which

| Aspect | Tuple | List |
|--------|-------|------|
| Mutability | Immutable | Mutable |
| Intended use | Fixed structure (record) | Variable-length sequence |
| Memory | Smaller (no over-allocation) | Larger (over-allocated) |
| Hashable | Yes (if all items hashable) | No |
| Can be dict key | Yes | No |
| Unpacking | Natural (record semantics) | Also works |

**Fluent Python rule:** Use tuples for **records** (fixed number of fields, each with meaning by position). Use lists for **homogeneous sequences** (variable number of items, all same type).

### Named Tuples

```python
from collections import namedtuple

# Define
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)

# Access
p.x              # 3 (named access)
p[0]             # 3 (positional access — still works)
x, y = p         # unpacking

# Methods
p._asdict()      # {'x': 3, 'y': 4} — for serialization
p._replace(x=5)  # Point(5, 4) — returns new instance
p._fields        # ('x', 'y') — field names

# Typed variant (Python 3.6+)
from typing import NamedTuple
class Point(NamedTuple):
    x: float
    y: float
    label: str = ""   # default works
```

**Why named tuples:**
- Self-documenting (field names, not magic indices)
- Memory-efficient (same as regular tuples — no `__dict__`)
- Immutable and hashable (dict-key-safe)
- Backward compatible with regular tuples

---

## 2.5 Array — Homogeneous Numeric Sequences

`array.array` is a type-constrained sequence — all elements must be the same type. More memory-efficient than list for large numeric datasets.

```python
from array import array

# Type codes: 'i' = signed int, 'f' = float, 'd' = double, 'u' = unicode
nums = array('i', [1, 2, 3, 4, 5])

nums.append(6)
nums.extend([7, 8])
nums[0]           # 1
nums[0:3]         # array('i', [1, 2, 3])

# Type error
nums.append(3.14)  # TypeError — 'i' expects int
```

**Key type codes:**

| Code | C Type | Python Type | Size (bytes) |
|------|--------|-------------|--------------|
| `'b'` | signed char | int | 1 |
| `'h'` | short | int | 2 |
| `'i'` | int | int | 4 |
| `'l'` | long | int | 8 |
| `'f'` | float | float | 4 |
| `'d'` | double | float | 8 |

**File I/O:** `array` supports `tofile()` and `fromfile()` — fast binary read/write.

```python
# Fast binary I/O
nums = array('d', [1.5, 2.5, 3.5])
with open('data.bin', 'wb') as f:
    nums.tofile(f)

# Read back
restored = array('d')
with open('data.bin', 'rb') as f:
    restored.fromfile(f, 3)  # read 3 items
```

**When to use array:**
- Tens of thousands of numeric values
- Need type safety (prevent accidental mixed types)
- Fast binary I/O is a requirement
- But for pure number-crunching → NumPy

---

## 2.6 Deque — Double-Ended Queue

`collections.deque` is a thread-safe, memory-efficient double-ended queue. O(1) append/pop on **both** ends.

```python
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)           # Right end — [1, 2, 3, 4]
dq.appendleft(0)       # Left end — [0, 1, 2, 3, 4]
dq.pop()               # 4 — from right
dq.popleft()           # 0 — from left (O(1) — unlike list)

# Bounded deque (fixed max length — drops from opposite end)
dq = deque(maxlen=3)
dq.append(1)           # [1]
dq.append(2)           # [1, 2]
dq.append(3)           # [1, 2, 3]
dq.append(4)           # [2, 3, 4] — 1 is dropped!

# Rotate
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)           # [4, 5, 1, 2, 3] — positive = right rotation
dq.rotate(-1)          # [5, 1, 2, 3, 4]

# Extend
dq.extend([6, 7])      # Right extend
dq.extendleft([0, -1]) # Left extend (reversed order)
```

**Bounded deque use case:** Keep the last N items (log tail, recent commands, sliding window).

| Operation | list | deque |
|-----------|------|-------|
| `append` | O(1)* | O(1) |
| `appendleft` | O(n) | O(1) |
| `pop` | O(1) | O(1) |
| `popleft` | O(n) | O(1) |
| `insert` | O(n) | O(n) |
| Indexing | O(1) | O(n) |
| Memory | Over-allocation | Block-based |

**Trade-off:** deque is great as a queue but slow for random access (O(n)). Don't use it as a general list replacement.

---

## 2.7 bisect — Maintaining Sorted Lists

The `bisect` module works with sorted lists — finding insertion points and inserting while keeping order.

```python
import bisect

grades = [60, 70, 80, 90]

# Find insertion point
bisect.bisect(grades, 75)       # 2 (keep right on ties)
bisect.bisect_left(grades, 75)  # 2 (keep left on ties)

# Insert while preserving sort
bisect.insort(grades, 75)       # [60, 70, 75, 80, 90]
bisect.insort_left(grades, 75)  # same, but inserts left of equal values
```

### Scored lookup pattern (grade boundaries)

```python
def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect.bisect(breakpoints, score)
    return grades[i]

[grade(s) for s in [33, 55, 70, 82, 99]]  # ['F', 'F', 'D', 'B', 'A']
```

### Performance considerations

| Operation | List + bisect | Sorted container |
|-----------|---------------|------------------|
| Search (bisect) | O(log n) | O(log n) |
| Insert (insort) | O(n) — shift | O(log n) |
| In-order iteration | O(n) | O(n) |

**Trade-off:** `bisect.insort` is O(n) because it shifts elements. For large datasets with many inserts, consider `sortedcontainers` (third-party) or a binary search tree.

---

## 2.8 memoryview & struct — Binary Data

`memoryview` exposes an object's buffer protocol without copying. Essential for binary data processing.

```python
# memoryview — zero-copy access to buffer
data = bytearray(b"Hello World")
view = memoryview(data)
view[0]               # 72 (int, ASCII 'H')
view[0] = 104         # Mutates original buffer!
view[6:11].tobytes()  # b'World' — still no full copy

# Cast (reinterpret binary)
nums = array('h', [-2, -1, 0, 1, 2])  # signed short
memv = memoryview(nums)
memv_oct = memv.cast('B')            # reinterpret as unsigned byte
memv_oct.tolist()                    # [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
```

### struct — Packing/Unpacking Binary

```python
import struct

# Pack Python values → bytes
data = struct.pack('>i4sh', 7, b'spam', 8)
# > = big-endian, i = int, 4s = 4-char bytes, h = short

# Unpack bytes → Python values
unpacked = struct.unpack('>i4sh', data)
# (7, b'spam', 8)

# Format strings
fmt = struct.Struct('>i4sh')     # Pre-compiled for reuse
fmt.pack(7, b'spam', 8)
fmt.unpack(data)
fmt.size                          # 10 bytes
```

**Common format specifiers:**

| Specifier | C Type | Python | Size |
|-----------|--------|--------|------|
| `x` | pad byte | — | 1 |
| `b`/`B` | signed/unsigned char | int | 1 |
| `h`/`H` | signed/unsigned short | int | 2 |
| `i`/`I` | signed/unsigned int | int | 4 |
| `l`/`L` | signed/unsigned long | int | 8 |
| `f` | float | float | 4 |
| `d` | double | float | 8 |
| `s` | char[] | bytes | length |

**Byte order:** `>` (big-endian), `<` (little-endian), `!` (network = big-endian), `=` (native), `@` (native + alignment).

---

## 2.9 Advanced Slicing Patterns

### Reverse a Sequence

```python
seq[::-1]           # reverse — works on any sequence
list(reversed(seq)) # using reversed() — more readable
```

### Every Nth Element

```python
seq[::3]            # every 3rd element
seq[1::3]           # starting from index 1, every 3rd
```

### Remove Every Nth Element (del)

```python
del seq[::2]        # remove every other element — in-place on list
```

### Assign to Strided Slice

```python
nums = [0] * 10
nums[::2] = range(5)   # [0, 1, 0, 3, 0, 5, 0, 7, 0, 9] — on even positions

# Length must match:
nums[::3] = [1, 2, 3]  # 3 items for 3 positions
```

### Rolling Window (Slice + Zip)

```python
def rolling_window(seq, n=3):
    return list(zip(*(seq[i:] for i in range(n))))

rolling_window([1, 2, 3, 4, 5], 3)
# [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

### Split at a Point

```python
def split_at(seq, i):
    return seq[:i], seq[i:]

head, tail = split_at([1, 2, 3, 4, 5], 3)
# head = [1, 2, 3], tail = [4, 5]
```

---

## 2.10 Tuples as Immutable Records

### Record Unpacking Patterns

```python
records = [
    ("Melika", "Python", 95),
    ("Ali", "SQL", 88),
    ("Sara", "Pandas", 92),
]

# Classic unpacking in loop
for name, course, score in records:
    print(f"{name} scored {score} in {course}")

# Extended unpacking with *
first, *rest = records
# first = ("Melika", "Python", 95)
# rest = [("Ali", "SQL", 88), ("Sara", "Pandas", 92)]
```

### Fluent Python Unpacking Patterns

```python
# Divergent unpacking — catch all remaining
a, b, *rest = range(5)     # a=0, b=1, rest=[2, 3, 4]

# Ignore middle
a, *_, d = range(5)         # a=0, d=4, _=[1, 2, 3]

# Star in function calls
def f(a, b, c, d):
    return a + b + c + d

f(1, *[2, 3], 4)           # 10 — unpack mid-argument

# Nested unpacking
record = ("Melika", (1999, 7, 25))
name, (year, month, day) = record
```

---

## 2.11 Sequence Type Hierarchy (Fluent Python)

Fluent Python categorizes sequences along two axes:

### By Mutability

| | Mutable | Immutable |
|---|---|---|
| **Built-in** | `list`, `bytearray`, `array.array` | `tuple`, `str`, `bytes` |

### By Content Type

| | Container (mixes types) | Flat (single type) |
|---|---|---|
| **Mutable** | `list`, `collections.deque` | `bytearray`, `array.array`, `memoryview` |
| **Immutable** | `tuple` | `str`, `bytes` |

**Container sequences** hold references to objects — can hold different types. **Flat sequences** store values directly — more memory-efficient but limited to one type.

---

## 2.12 Practice Checklist

- [ ] Create lists with comprehension, repetition, and constructor
- [ ] Use slicing with all three components `[start:stop:step]`
- [ ] Assign to slices (replace, insert, delete)
- [ ] Create named tuples and use field access + unpacking
- [ ] Use `bisect` for sorted-list insertion and search
- [ ] Compare `list` vs `deque` performance for stack vs queue
- [ ] Use `array.array` for memory-efficient numeric storage
- [ ] Pack/unpack binary data with `struct`
- [ ] Use `memoryview` for zero-copy buffer access
- [ ] Implement `__getitem__` and `__len__` in a custom class

---

## Flashcards

See: [flashcards.md](../flashcards.md), [flashcards-fa.md](../flashcards-fa.md)

## Progress

- [ ] Read Fluent Python Ch 2 — An Array of Sequences
- [ ] Practice: slicing, named tuples, bisect, array, deque
- [ ] Implement a custom sequence class
- [ ] Master the bisect module for sorted sequences
