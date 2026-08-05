# Ch 6: Comprehensions, Lambda & Functional Tools

## Books Covered
- **Fluent Python (2nd Ed)** — Ch 2: Arrays of Sequences (list comprehensions, generator expressions, dict/set comprehensions)
- **Effective Python (3rd Ed)** — Items 5–8: comprehensions, generator expressions, lambda functions, functional tools
- **Python Cookbook (3rd Ed)** — Ch 1: Data Structures & Algorithms (list/dict/set comprehensions, functional patterns)

## Roadmap Sections Covered
- ✅ List, dict, set comprehensions
- ✅ Generator expressions vs list comprehensions
- ✅ Nested comprehensions & flattening
- ✅ Lambda functions & use cases
- ✅ Functional tools: `map`, `filter`, `reduce`, `functools.partial`
- ✅ `itertools` — `chain`, `islice`, `cycle`, `repeat`, `groupby`, `product`, `permutations`, `combinations`
- ✅ `operator` module — `itemgetter`, `attrgetter`, `methodcaller`

---

## 6.1 List Comprehensions

List comprehensions provide a concise way to create lists. More Pythonic than `map`/`filter` with lambdas.

### Basic Syntax

```python
[expr for item in iterable if condition]
```

```python
# Basic
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Transform + filter
words = ["apple", "banana", "cherry"]
lengths = [len(w) for w in words if len(w) > 5]
# [6, 6]
```

### Nested Comprehensions (Flattening)

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten — outer loop first, inner loop second
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Equivalent nested for loops
flat = []
for row in matrix:
    for x in row:
        flat.append(x)
```

**Order rule:** write loops in the same order as nested `for` loops.

### Multiple `for` clauses (Cartesian product)

```python
colors = ["red", "blue"]
sizes = ["S", "M", "L"]

combos = [(c, s) for c in colors for s in sizes]
# [('red', 'S'), ('red', 'M'), ('red', 'L'), ('blue', 'S'), ...]

# Equivalent to itertools.product
from itertools import product
list(product(colors, sizes))
```

---

## 6.2 Dict & Set Comprehensions

### Dict Comprehension

```python
# {key_expr: value_expr for item in iterable if condition}
words = ["apple", "banana", "cherry"]
word_len = {w: len(w) for w in words}
# {'apple': 5, 'banana': 6, 'cherry': 6}

# Invert a dict (assumes unique values)
d = {"a": 1, "b": 2}
inverted = {v: k for k, v in d.items()}
# {1: 'a', 2: 'b'}

# Filter + transform
{word: len(word) for word in words if len(word) > 5}
# {'banana': 6, 'cherry': 6}
```

### Set Comprehension

```python
# {expr for item in iterable if condition}
words = ["apple", "banana", "cherry"]
unique_lengths = {len(w) for w in words}
# {5, 6}

# From list with duplicates
nums = [1, 2, 2, 3, 3, 3]
unique = {x for x in nums}
# {1, 2, 3}
```

---

## 6.3 Generator Expressions

Generator expressions look like list comprehensions but use parentheses and produce **lazy iterators** — memory efficient for large sequences.

```python
# List comprehension — creates full list in memory
squares_list = [x**2 for x in range(1_000_000)]  # ~8 MB

# Generator expression — yields one at a time
squares_gen = (x**2 for x in range(1_000_000))   # ~200 bytes

next(squares_gen)  # 0
next(squares_gen)  # 1
```

### When to Use Each

| Use Generator Expression | Use List Comprehension |
|---|---|
| Large/infinite sequences | Need random access / multiple passes |
| Chaining operations (pipeline) | Small, bounded data |
| Memory-constrained | Need `len()` or indexing |

### Generator Expression vs List Comprehension in Function Calls

```python
# These are equivalent — parens optional when sole argument
sum(x**2 for x in range(10))      # generator expression
sum([x**2 for x in range(10)])    # list comprehension (wastes memory)

# But you need parens in other contexts
list(x**2 for x in range(5))      # generator
# (x**2 for x in range(5))        # syntax error — ambiguous
```

---

## 6.4 Lambda Functions

`lambda` creates anonymous functions — limited to a **single expression**.

```python
# lambda args: expression
square = lambda x: x**2
square(5)              # 25

# Multiple args
add = lambda a, b: a + b
add(2, 3)              # 5

# Default args
mult = lambda a, b=2: a * b
mult(3)                # 6
mult(3, 4)             # 12
```

### Common Use Cases

```python
# Key functions for sorting
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
sorted(students, key=lambda s: s[1])       # sort by score
# [('Charlie', 78), ('Alice', 85), ('Bob', 92)]

# map / filter (though comprehensions often preferred)
list(map(lambda x: x*2, [1,2,3]))          # [2, 4, 6]
list(filter(lambda x: x%2==0, range(10)))  # [0, 2, 4, 6, 8]

# functools.partial — fix some args
from functools import partial
mul2 = partial(lambda a, b: a*b, 2)
mul2(5)                                    # 10
```

### Lambda Gotchas

**Late binding in loops:**
```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]        # [2, 2, 2] — all capture same variable!

# Fix: bind as default
funcs = [lambda i=i: i for i in range(3)]
[f() for f in funcs]        # [0, 1, 2]
```

**Cannot contain statements:**
```python
# ❌ lambda: for i in range(3): print(i)   # SyntaxError
# ✅ def f(): for i in range(3): print(i)
```

**Prefer `def` when:**
- Function needs a name for readability
- Multiple statements needed
- Recursion needed
- Docstring/type hints needed

---

## 6.5 Functional Tools

### `map(func, iterable, ...)`

Applies function to each item of iterable(s). Returns iterator.

```python
list(map(str.upper, ["a", "b", "c"]))     # ['A', 'B', 'C']
list(map(lambda x, y: x + y, [1,2], [10,20]))  # [11, 22] — stops at shortest
```

### `filter(func, iterable)`

Returns iterator of items where function returns truthy.

```python
list(filter(lambda x: x > 5, range(10)))   # [6, 7, 8, 9]
list(filter(None, [0, 1, "", "a", []]))    # [1, 'a'] — filter falsy
```

### `functools.reduce(func, iterable[, initializer])`

Cumulatively applies function to items. Reduces to single value.

```python
from functools import reduce

reduce(lambda a, b: a + b, [1,2,3,4,5])    # 15 (sum)
reduce(lambda a, b: a * b, [1,2,3,4])      # 24 (product)

# With initializer
reduce(lambda a, b: a + b, [], 0)          # 0 (empty case)
reduce(lambda a, b: a + b, [1], 10)        # 11
```

**`operator` module alternatives (faster, more readable):**
```python
from operator import add, mul
reduce(add, [1,2,3,4])    # 10
reduce(mul, [1,2,3,4])    # 24
```

### `functools.partial(func, *args, **keywords)`

Creates a new function with some arguments pre-filled.

```python
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)

square(5)      # 25
cube(3)        # 27

# Common pattern: pre-configure functions
from operator import itemgetter
get_name = itemgetter("name")
users = [{"name": "Alice"}, {"name": "Bob"}]
list(map(get_name, users))    # ['Alice', 'Bob']
```

---

## 6.6 `itertools` — Infinite & Combinatorial Iterators

`itertools` provides fast, memory-efficient iterator tools.

### Infinite Iterators

```python
from itertools import count, cycle, repeat

# count(start, step) — infinite counter
list(zip(count(), ['a', 'b', 'c']))      # [(0, 'a'), (1, 'b'), (2, 'c')]

# cycle(iterable) — infinite repetition
list(islice(cycle([1, 2]), 5))           # [1, 2, 1, 2, 1]

# repeat(elem, [n]) — n times (or infinite)
list(repeat("x", 3))                     # ['x', 'x', 'x']
```

### Terminating Iterators

```python
from itertools import islice, takewhile, dropwhile, chain, compress

# islice(iterable, start, stop[, step]) — slice an iterator
list(islice(range(100), 5, 15))          # [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

# takewhile / dropwhile
list(takewhile(lambda x: x < 5, range(10)))  # [0, 1, 2, 3, 4]
list(dropwhile(lambda x: x < 5, range(10)))  # [5, 6, 7, 8, 9]

# chain(*iterables) — concatenate iterables
list(chain([1,2], [3,4], [5]))           # [1, 2, 3, 4, 5]

# compress(data, selectors) — filter by boolean mask
data = ['a', 'b', 'c', 'd']
mask = [True, False, True, False]
list(compress(data, mask))               # ['a', 'c']
```

### Combinatorial Iterators

```python
from itertools import product, permutations, combinations, combinations_with_replacement

items = ['a', 'b', 'c']

# product — Cartesian product (with replacement, ordered)
list(product(items, repeat=2))
# [('a','a'), ('a','b'), ('a','c'), ('b','a'), ...]

# permutations — ordered, no replacement
list(permutations(items, 2))
# [('a','b'), ('a','c'), ('b','a'), ('b','c'), ('c','a'), ('c','b')]

# combinations — unordered, no replacement
list(combinations(items, 2))
# [('a','b'), ('a','c'), ('b','c')]

# combinations_with_replacement — unordered, with replacement
list(combinations_with_replacement(items, 2))
# [('a','a'), ('a','b'), ('a','c'), ('b','b'), ('b','c'), ('c','c')]
```

### Grouping & Aggregation

```python
from itertools import groupby

data = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]

# Must sort by key first!
data_sorted = sorted(data, key=lambda x: x[0])

for key, group in groupby(data_sorted, key=lambda x: x[0]):
    print(key, list(group))
# fruit [('fruit', 'apple'), ('fruit', 'banana')]
# veg [('veg', 'carrot')]
```

---

## 6.7 `operator` Module — Functional Alternatives to Lambdas

Functions for common operations — faster and more readable than lambdas.

```python
from operator import itemgetter, attrgetter, methodcaller, add, mul

# itemgetter — extract item by index/key
data = [("a", 3), ("b", 1), ("c", 2)]
sorted(data, key=itemgetter(1))              # [('b', 1), ('c', 2), ('a', 3)]
user = {"name": "Alice", "age": 30}
itemgetter("name")(user)                     # 'Alice'

# attrgetter — extract attribute
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [Person("Alice", 30), Person("Bob", 25)]
sorted(people, key=attrgetter("age"))        # sort by age

# methodcaller — call method by name
text = "hello world"
methodcaller("upper")(text)                  # 'HELLO WORLD'
methodcaller("replace", " ", "-")(text)      # 'hello-world'

# Arithmetic operators
add(1, 2)       # 3
mul(3, 4)       # 12
```

---

## 6.8 Practical Patterns

### Pipeline with `map`/`filter`/`reduce`

```python
from functools import reduce
from operator import add

numbers = range(1, 11)

# Sum of squares of even numbers
result = reduce(
    add,
    map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers))
)
# 4 + 16 + 36 + 64 + 100 = 220
```

### Dict of Lists — Grouping with Comprehension

```python
data = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]

# Group by key using dict comprehension
groups = {k: [v for k2, v in data if k2 == k] for k in set(k for k, _ in data)}
# {'fruit': ['apple', 'banana'], 'veg': ['carrot']}

# Better: use itertools.groupby (requires sorted)
from itertools import groupby
data_sorted = sorted(data, key=lambda x: x[0])
groups = {k: [v for _, v in g] for k, g in groupby(data_sorted, key=lambda x: x[0])}
```

### Flattening Nested Structures

```python
# List of lists
matrix = [[1,2], [3,4], [5,6]]
flat = [x for row in matrix for x in row]

# Dict of lists
d = {"a": [1,2], "b": [3,4]}
flat = [x for lst in d.values() for x in lst]

# Using itertools.chain
from itertools import chain
flat = list(chain.from_iterable(matrix))
flat = list(chain.from_iterable(d.values()))
```

---

## 6.9 Interview Q&A

**Q: What's the difference between a list comprehension and a generator expression?**
A: List comprehension creates the full list in memory immediately. Generator expression returns a lazy iterator that yields one item at a time — memory efficient for large/infinite sequences.

**Q: When would you use `lambda` vs `def`?**
A: `lambda` for short, throwaway functions (e.g., `key=`, `func=` arguments). `def` for reusable, named functions, multiple statements, recursion, docstrings, type hints.

**Q: What's the late-binding gotcha with lambdas in loops?**
A: Lambdas capture the *variable*, not its value at creation time. All lambdas reference the same variable, which has the final loop value. Fix: `lambda i=i: i` (bind as default).

**Q: What does `functools.reduce` do?**
A: Cumulatively applies a binary function to items of an iterable, reducing to a single value. `reduce(lambda a,b: a+b, [1,2,3])` → `((1+2)+3)` = 6.

**Q: What's the difference between `itertools.product`, `permutations`, and `combinations`?**
A: `product` = Cartesian product (ordered, with replacement). `permutations` = ordered, no replacement. `combinations` = unordered, no replacement.

**Q: How does `operator.itemgetter` work?**
A: Returns a callable that extracts an item by index/key: `itemgetter(1)(["a", "b"])` → `"b"`. Faster than `lambda x: x[1]` and works with `sorted(key=)`.

**Q: What does `itertools.groupby` require?**
A: Input must be pre-sorted by the grouping key. Groups consecutive items with the same key.

**Q: When is `functools.partial` useful?**
A: Pre-filling arguments to create specialized functions. E.g., `partial(open, encoding='utf-8')` creates a version of `open` that defaults to UTF-8.

---

## Key Takeaways

1. **List comprehensions** — most Pythonic for simple transformations/filters. Read left-to-right like English.
2. **Generator expressions** — use for large/infinite sequences, memory efficiency, chaining.
3. **Dict/set comprehensions** — same syntax, curly braces. Great for inversion, deduping.
4. **Nested comprehensions** — write loops in same order as nested `for`. Good for flattening.
5. **Lambda** — single expression, anonymous. Best for `key=`/`func=` arguments. Avoid in loops (late binding).
6. **`map`/`filter`/`reduce`** — functional tools. Often comprehensions are more readable.
7. **`itertools`** — infinite iterators (`count`, `cycle`, `repeat`), slicing (`islice`), combinatorial (`product`, `permutations`, `combinations`), grouping (`groupby`).
8. **`operator` module** — `itemgetter`, `attrgetter`, `methodcaller`, `add`, `mul` — faster and more readable than equivalent lambdas.
9. **`functools.partial`** — fix arguments to create specialized functions.

---

## Flashcards

See: [flashcards.md](../flashcards.md), [flashcards-fa.md](../flashcards-fa.md)

## Progress

- [ ] Read Fluent Python Ch 2 — Arrays of Sequences
- [ ] Read Effective Python Items 5–8 — comprehensions, generators, lambdas, functional tools
- [ ] Read Python Cookbook Ch 1 — Data Structures & Algorithms
- [ ] Practice: list/dict/set comprehensions, generator expressions
- [ ] Practice: itertools.product/permutations/combinations, groupby
- [ ] Practice: operator.itemgetter/attrgetter, functools.partial/reduce
