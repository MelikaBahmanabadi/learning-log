# Python Flashcards — EN

## Ch 1: Python Basics & Environment

Q: Pythonic way to open a file?
A: `with open(path) as fh:` — context manager auto-closes.

Q: EAFP vs LBYL?
A: EAFP (Easier to Ask Forgiveness) — try/except, Pythonic. LBYL (Look Before You Leap) — if checks.

Q: How to create a venv?
A: `python -m venv .venv && source .venv/bin/activate`

Q: What's the modern project config file?
A: `pyproject.toml` (PEP 517/518/621).

Q: Truthiness: what values are falsy?
A: `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`, `False`.

Q: How to swap two variables?
A: `a, b = b, a` — tuple unpacking.

Q: What's the Pythonic way to get index + value?
A: `for i, v in enumerate(sequence):`

Q: How to iterate two sequences together?
A: `for a, b in zip(xs, ys):`

Q: What's the walrus operator `:=`?
A: Assignment expression — assign AND use in expression: `if (data := get_data()):`

Q: What does `sorted(items, key=lambda x: x[1])` do?
A: Sort items by second element of each item.

Q: What's the mutable default argument gotcha?
A: `def f(lst=[])` — list is shared across calls. Use `def f(lst=None)` + `if lst is None: lst = []`.

Q: What are positional-only params?
A: `/` in function signature — params before `/` can't be passed as keyword: `def div(a, b, /):`

Q: What are keyword-only params?
A: `*` in function signature — params after `*` must be passed as keyword: `def f(a, *, kw_only):`

Q: What's `if __name__ == "__main__"` for?
A: Run code only when script is executed directly, not when imported.

Q: PEP 8 function naming?
A: `snake_case`

Q: PEP 8 class naming?
A: `PascalCase`

Q: How to handle mutable default args safely?
A: Use `None` as default, create fresh mutable inside: `def f(items=None): items = items or []`

Q: What's the LEGB rule?
A: Local → Enclosing → Global → Built-in — Python's name resolution order.

Q: What does `match/case` do? (Python 3.10+)
A: Structural pattern matching — `match command.split(): case ["quit"]: ...`

Q: How to read a file line-by-line memory-efficiently?
A: `for line in file:` — reads one line at a time.

Q: What's the difference between `is` and `==`?
A: `is` checks identity (same object); `==` checks value equality.

Q: What does a list comprehension look like?
A: `[x**2 for x in range(10) if x % 2 == 0]`

Q: Dict comprehension example?
A: `{x: x**2 for x in range(5)}`

Q: Set comprehension example?
A: `{x for x in range(20) if x % 2 == 0}`

Q: How to flatten a list of lists with comprehension?
A: `[x for row in matrix for x in row]`

Q: What's the `else` clause on a `for` loop?
A: Runs if loop completed without `break` — useful for search loops.

Q: How to iterate over dict key-value pairs?
A: `for k, v in dict.items():`

Q: f-string format for 2 decimal places?
A: `f"{value:.2f}"`

Q: f-string to zero-pad width 4?
A: `f"{value:04d}"`

Q: pathlib: how to join paths?
A: `Path("folder") / "sub" / "file.txt"`

Q: How to copy a list?
A: `new_list = old_list.copy()` or `new_list = old_list[:]`

Q: What's the set difference operator?
A: `a - b` — elements in `a` but not in `b`.

Q: What's the dict merge operator (Python 3.9+)?
A: `dict1 | dict2`

Q: How to safely get a dict key with default?
A: `dict.get("key", "default")`

---

## Ch 2: Sequences, Lists, Tuples & Slicing

Q: What's the difference between `list` and `tuple`?
A: list is mutable, tuple is immutable. tuple uses less memory, can be a dict key, and represents a fixed record. list over-allocates for efficient append.

Q: How does slicing `[start:stop:step]` work?
A: start = inclusive first index, stop = exclusive end index, step = stride. Negative step reverses direction. All three are optional.

Q: What does `seq[::-1]` do?
A: Reverses the sequence — negative step with omitted start/stop traverses backwards.

Q: How do you assign to a slice?
A: `list[2:5] = [100, 200]` replaces items 2–5 with new items. Can change list length. Step-slice assignment requires matching lengths.

Q: How do you insert into a list at position i using slices?
A: `list[i:i] = [item]` — inserts item at index i without removing anything.

Q: What is a slice object?
A: `slice(start, stop, step)` — created implicitly by `seq[1:5:2]`. Can be named and reused: `s = slice(1, 5, 2); seq[s]`.

Q: What's the time complexity of `list.append()`?
A: O(1) amortized — list over-allocates capacity so most appends don't reallocate.

Q: What's the time complexity of `list.pop(0)`?
A: O(n) — all remaining elements shift left. Use `collections.deque.popleft()` for O(1).

Q: What is a `namedtuple`?
A: `namedtuple("Point", ["x", "y"])` creates a tuple subclass with named fields. Access by name (`p.x`) or position (`p[0]`). Immutable, hashable, memory-efficient.

Q: When to use `array.array` vs `list`?
A: `array.array` for large homogeneous numeric data — memory-efficient, type-safe, fast binary I/O. List for heterogeneous or mixed-type data.

Q: What does `collections.deque` offer over `list`?
A: O(1) `append`/`popleft` on BOTH ends. List has O(n) `pop(0)`. deque is ideal for queues, sliding windows, and bounded buffers (`maxlen`).

Q: How does `bisect.insort` work?
A: Finds insertion point via binary search (O(log n)), then inserts (O(n) shift). Keeps list sorted.

Q: What does `bisect.bisect_left` vs `bisect.bisect` differ on?
A: `bisect_left` returns leftmost insertion point (before existing equal values). `bisect` returns rightmost (after equal values).

Q: How do you create a bounded deque that drops old items?
A: `deque(maxlen=5)` — when full, new append drops the item on the opposite end.

Q: What's the sequence protocol?
A: Implement `__len__` and `__getitem__` — makes any class support slicing, iteration, `in`, `reversed()`.

Q: What's `struct.pack` used for?
A: Pack Python values into binary bytes according to a format string: `struct.pack('>i4sh', 7, b'spam', 8)`.

Q: What's `memoryview` for?
A: Zero-copy access to an object's buffer — view and mutate bytes without copying the underlying data.

Q: What's the tuple packing vs unpacking syntax?
A: Packing: `t = 1, 2, 3` → tuple `(1, 2, 3)`. Unpacking: `a, b, c = t` → individual variables.

Q: How do named tuples compare to regular tuples for serialization?
A: Named tuples have `._asdict()` method for dict conversion. Same memory footprint as regular tuples.

Q: What happens if you assign to a tuple?
A: `TypeError` — tuples are immutable. But if a tuple contains a mutable object, that object CAN be mutated.

Q: How do you reverse a list in-place vs create a reversed copy?
A: `list.reverse()` reverses in-place (returns None). `reversed(seq)` returns an iterator. `seq[::-1]` creates a new reversed list.

Q: What does `seq[::2]` return?
A: Every second element from the sequence.

Q: How do you split a sequence at a point?
A: `head, tail = seq[:i], seq[i:]`

Q: What is `Ellipsis` (`...`) used for in Python?
A: In custom containers and NumPy: `arr[..., 0]` means "all previous dimensions, then column 0".

Q: What's the difference between container and flat sequences?
A: Container sequences (list, tuple, deque) hold references = can mix types. Flat sequences (str, bytes, array) store values directly = memory-efficient, one type.

Q: When should you use `collections.deque` for a queue?
A: FIFO queue — `deque` gives O(1) `popleft`. list gives O(n) `pop(0)`. For thread-safe queue, use `queue.Queue`.

Q: What is a rolling window pattern with zip?
A: `list(zip(*(seq[i:] for i in range(n))))` — produces n-length tuples sliding over the sequence.
