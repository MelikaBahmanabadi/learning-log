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

---

## Ch 3: Dicts, Sets & Mapping Structures

Q: How do you create a dict with default values for missing keys?
A: `d.get("key", "default")` — returns default without KeyError. For automatic defaults: `collections.defaultdict(list)`.

Q: What's the difference between `d.get(k)` and `d.setdefault(k, default)`?
A: `get` returns default but doesn't modify dict. `setdefault` inserts default if key missing, then returns value. `setdefault` always evaluates default argument (no lazy evaluation).

Q: How does `defaultdict` work?
A: Takes a factory function. When missing key accessed via `d[key]`, factory is called to produce default: `defaultdict(list)` creates empty list, `defaultdict(int)` creates 0.

Q: What's `collections.Counter`?
A: Dict subclass for counting hashable objects. `c = Counter("abracadabra")` → counts each char. Has `most_common(n)`, arithmetic (`+`, `-`, `&`, `|`), `elements()`.

Q: How do you merge two dicts (Python 3.9+)?
A: `merged = d1 | d2` (new dict). `d1 |= d2` (in-place). Later keys win on conflict.

Q: What's the `__missing__` hook?
A: Method on dict subclass called when `d[key]` raises KeyError. Lets you handle missing keys dynamically: `class AutoDict(dict): def __missing__(self, k): return 0`.

Q: What's `collections.OrderedDict` good for when regular dict is already ordered?
A: `move_to_end(key)` and order-sensitive equality (`od1 == od2` checks position, regular dict doesn't). Otherwise regular dict (3.7+) suffices.

Q: What's `collections.ChainMap`?
A: Groups multiple dicts into single view. Lookups search each dict in order. Mutations affect only the first dict. Good for config layering (CLI args > env > defaults).

Q: What types are hashable in Python?
A: Immutable types: int, float, str, bytes, tuple (if all elements hashable), frozenset. Mutable types (list, set, dict) are NOT hashable. User objects are hashable by default (by id).

Q: Time complexity of `key in dict` vs `key in list`?
A: `key in dict` — O(1) average (hash table). `key in list` — O(n) (linear scan). Use set/dict for large membership checks.

Q: What's the difference between `set` and `frozenset`?
A: `set` is mutable (add/remove/discard/update). `frozenset` is immutable and hashable — can be used as dict key or inside another set.

Q: Set operations: union vs intersection vs difference?
A: `a | b` — union (all elements). `a & b` — intersection (common). `a - b` — difference (in a not b). `a ^ b` — symmetric diff (in either, not both).

Q: How do you check if a is a subset of b?
A: `a <= b` or `a.issubset(b)`. For proper subset: `a < b`.

Q: What's `MappingProxyType`?
A: Wraps a dict as read-only. `MappingProxyType({"key": "val"})` — prevents mutation. Useful for exposing internal dicts as API.

Q: What's the danger of using a mutable object as dict key?
A: If the object mutates after insertion, its hash changes. The dict can't find it anymore (`KeyError`), and the old entry leaks as garbage.

Q: How do you invert a dict (swap keys and values)?
A: `{v: k for k, v in d.items()}`. If values aren't unique, later keys overwrite earlier ones — use `defaultdict(list)` to collect.

Q: How do you group items from a list of tuples using dict?
A: `defaultdict(list)` — `groups[lang].append(name)`. Group people by language, files by extension, etc.

Q: What does `Counter("abracadabra").most_common(3)` return?
A: `[("a", 5), ("b", 2), ("r", 2)]` — top 3 most frequent elements with counts.

Q: What's the difference between `set.discard` and `set.remove`?
A: `remove(x)` raises KeyError if x missing. `discard(x)` is a no-op if x missing (no error).

Q: How does Python's dict handle hash collisions?
A: Open addressing — probes next slots until finding empty slot. When load factor exceeds ~2/3, the table resizes to reduce collisions.

Q: What's the difference between `UserDict` and direct `dict` subclassing?
A: `UserDict` wraps `self.data` dict — `update()` and `__init__()` route through your overrides. `dict` subclass bypasses overrides in some methods. Prefer `UserDict` for safety unless you have specific performance reasons for `dict`.

Q: What's `collections.abc.Mapping` and `MutableMapping`?
A: ABCs for dict-like classes. Implement 6 core methods (`__getitem__`, `__len__`, `__iter__`, `__contains__`, plus `__setitem__`/`__delitem__` for mutable) → get 20+ methods (keys, values, items, get, pop, update, clear) for free.

Q: Do `dict.keys()` and `dict.items()` support set operations?
A: Yes — `KeysView` and `ItemsView` implement the `Set` protocol. `d1.keys() & d2.keys()` → common keys. `d1.items() ^ d2.items()` → changed items. `d1.keys() - d2.keys()` → keys in d1 not in d2. `d.values()` does NOT (values may be unhashable).

Q: How do you find the key with min/max value in a dict?
A: `min(prices, key=prices.get)` — uses `dict.get` as key function. For sorted: `sorted(prices, key=prices.get)`. For (key, value) pairs: `min(prices.items(), key=lambda x: x[1])`.

Q: How do you deduplicate a list while preserving order?
A: `list(dict.fromkeys(items))` — Python 3.7+ dict preserves insertion order, `fromkeys` drops duplicates. For non-hashable items, use a set-based generator: `seen = set(); [x for x in items if not (x in seen or seen.add(x))]`.

---

## Ch 4: Strings, Bytes & Text Processing

Q: What's the difference between `str`, `bytes`, and `bytearray`?
A: `str` — immutable Unicode code points. `bytes` — immutable sequence of ints 0–255. `bytearray` — mutable bytes. `b"AB"[0]` → `65` (int); `"AB"[0]` → `"A"`.

Q: How do you convert between `str` and `bytes`?
A: `s.encode("utf-8")` → bytes (str → bytes at the I/O edge). `b.decode("utf-8")` → str. Never mix them with `+` or `==` — TypeError.

Q: What happens on `"é".encode("ascii")`?
A: `UnicodeEncodeError` — é not in ASCII. Use `errors="replace"`, `"ignore"`, or `"backslashreplace"`. For decoding, `b.decode("utf-8", errors="replace")` substitutes the � char.

Q: What is a code point and how do `ord()` / `chr()` work?
A: Code point = integer identifying a Unicode char. `ord("A")` → 65, `chr(65)` → "A". A code point's byte length depends on encoding — "é" is 2 bytes in UTF-8, 2 in UTF-16, 4 in UTF-32.

Q: What's the difference between UTF-8 and UTF-16?
A: UTF-8: 1–4 bytes, ASCII-compatible, web default. UTF-16: 2–4 bytes, needs BOM to signal byte order, legacy on Windows/Java. UTF-32: fixed 4 bytes, wasteful.

Q: Why does `"café" == "café"` evaluate to False, and how do you fix it?
A: Same visual text, different code points (precomposed é vs e + combining accent). Fix with `unicodedata.normalize("NFC", s)` — composes canonically. `NFD` decomposes.

Q: When should you use `casefold()` instead of `lower()`?
A: For case-insensitive comparison. `casefold()` handles German ß: `"Straße".casefold() == "strasse".casefold()` → True, but `lower()` → False.

Q: How do you strip accents from text?
A: `unicodedata.normalize("NFD", s)` then filter out `unicodedata.combining(c)` chars: `"".join(c for c in NFD(s) if not combining(c))`.

Q: How do you split a string on any whitespace run vs an exact separator?
A: `s.split()` — splits on any whitespace run, collapses. `s.split(",")` — exact separator. `s.split(",", maxsplit=1)` — limit. `rsplit` — from the right.

Q: What's the danger of `str.strip(chars)`?
A: It removes *any char in the set*, not a literal string — `"http://".strip("/")` strips every `/` at both ends. For literal suffixes use `removesuffix()` (Python 3.9+).

Q: What's the difference between `re.match` and `re.search`?
A: `match` anchors at the start of the string; `search` scans anywhere. Use `search` (or `fullmatch` for whole-string) in most cases.

Q: How do you capture groups with regex?
A: `(...)` captures. `re.findall(r"#(\d+)", text)` returns group contents. `(?P<name>...)` names a group → `m.group("name")` / `m.groupdict()`. `(?:...)` is non-capturing.

Q: How do you do regex find-and-replace with backreferences?
A: `re.sub(r"(\w+) (\w+)", r"\2 \1", "hello world")` → "world hello". Use `\1`, `\2` for groups in the replacement string.

Q: When should you use `re.escape`?
A: When building a regex from user/literal input: `re.escape("a.b*c")` → `a\.b\*c`, so special chars are matched literally.

Q: What's the correct way to open a text file with encoding?
A: `open("data.txt", encoding="utf-8")` — always pass `encoding=` explicitly (never rely on locale). Binary: `"rb"`/`"wb"`. For dirty data: `errors="replace"`.

Q: Why should you decode bytes at the I/O boundary?
A: Decode as soon as bytes enter your program (network, file) and encode just before they leave. Keep business logic in `str`, never mix the two.

Q: How do you collapse multiple whitespace runs into one space?
A: `" ".join(s.split())` — `split()` collapses every whitespace run, `join` rebuilds with single spaces.

Q: How do you collapse multiple whitespace characters?
A: `" ".join(s.split())` — split() collapses any whitespace run, join reassembles with single spaces.

Q: What's `str.casefold()` vs `str.lower()` for Turkish i?
A: Both are locale-independent, but `casefold()` is the stronger, Unicode-aware lowercase used for caseless matching — prefer it for `==`-style comparisons.

---

## Ch 5: Functions, Scope & Closures

Q: What's the mutable default argument gotcha?
A: Defaults evaluate once at def time — `def f(x, lst=[])` reuses the SAME list across calls. Fix: `def f(x, lst=None): lst = [] if lst is None else lst`.

Q: What do `*args` and `**kwargs` collect?
A: `*args` → tuple of extra positional args. `**kwargs` → dict of extra keyword args. Inverse: `f(*[1,2,3])` unpacks a list into positional, `f(**{"a":1})` unpacks a dict into keyword.

Q: How do you force keyword-only or positional-only parameters?
A: `def f(a, b, *, c)` — `*` makes everything after keyword-only. `def f(a, b, /)` — `/` makes everything before positional-only (Python 3.8+).

Q: What's the LEGB rule?
A: Name resolution order: Local → Enclosing → Global → Built-in. Assignment in a function makes a name local; reading falls back outward.

Q: What does `nonlocal` do vs `global`?
A: `nonlocal` rebinds a name from the enclosing function scope (needed to reassign a captured closure variable). `global` rebinds a module-level name. Avoid both when possible — return values instead.

Q: What is a closure?
A: A function plus the free variables it captures from its enclosing scope, kept alive after the enclosing function returns. `make_counter()` returning `counter()` that keeps its own `count`.

Q: What's the late-binding gotcha in loops?
A: A lambda/closure captures the *variable*, not its value: `[lambda: i for i in range(3)]` all return 2. Fix: bind as default `lambda i=i: i`.

Q: Why does `x = 10` before a `print(x)` in a function raise UnboundLocalError?
A: The later assignment makes `x` local to the whole function — Python decides scope at compile time, so the read can't see the global. Use `global x`.

Q: What's `functools.partial`?
A: Freezes part of a function's arguments: `partial(pow, 2)` → callable that takes one arg (exponent) and always uses base 2.

Q: What does `map`/`filter` return in Python 3?
A: Lazy iterators, not lists — wrap in `list()` to materialize: `list(map(f, xs))`, `list(filter(pred, xs))`. Use `sorted(xs, key=fn)` for ordering.

Q: What are first-class functions in Python?
A: Functions are objects: assignable (`g = f`), passable as args (`apply(f, x)`), returnable (`make_adder(5)` returns a closure), storable in lists/dicts.

Q: What's the recursion limit and why does it matter?
A: Default ~1000 (`sys.getrecursionlimit()`). Exceeding it raises `RecursionError`. Always have a base case; prefer iteration for deep recursion.

## Ch 6: Comprehensions, Lambda & Functional Tools

Q: What's the syntax for a list comprehension?
A: `[expr for item in iterable if condition]`

Q: How to flatten a 2D list with a list comprehension?
A: `[x for row in matrix for x in row]` — outer loop first, inner loop second.

Q: What's a dict comprehension?
A: `{key_expr: value_expr for item in iterable if condition}` — e.g., `{w: len(w) for w in words}`

Q: What's a set comprehension?
A: `{expr for item in iterable if condition}` — e.g., `{len(w) for w in words}` gives unique lengths.

Q: Difference between list comprehension and generator expression?
A: List comprehension creates full list in memory. Generator expression (`(...)`) yields lazily — memory efficient for large sequences.

Q: When to use generator expression vs list comprehension?
A: Generator for large/infinite sequences, chaining, memory-constrained. List for small data, need random access/len/indexing.

Q: How to sum squares using a generator expression?
A: `sum(x**2 for x in range(10))` — no extra brackets needed as sole argument.

Q: What's the lambda syntax?
A: `lambda args: expression` — single expression only, no statements.

Q: Lambda with default arguments?
A: `lambda a, b=2: a * b` — defaults evaluated at definition time.

Q: Common lambda use case?
A: `key=` functions: `sorted(items, key=lambda x: x[1])` or `map`/`filter` callbacks.

Q: Late-binding gotcha with lambdas in loops?
A: `funcs = [lambda: i for i in range(3)]` → all return 2. Fix: `lambda i=i: i` binds value as default.

Q: When to prefer `def` over `lambda`?
A: Named function needed, multiple statements, recursion, docstring/type hints, readability.

Q: What does `map(func, iterable)` do?
A: Returns iterator applying func to each item: `list(map(str.upper, ["a", "b"]))` → `["A", "B"]`.

Q: What does `filter(func, iterable)` do?
A: Returns iterator of items where func is truthy: `list(filter(lambda x: x>5, range(10)))` → `[6,7,8,9]`.

Q: What does `functools.reduce(func, iterable)` do?
A: Cumulatively applies binary function: `reduce(lambda a,b: a+b, [1,2,3])` → 6. With initializer: `reduce(add, [], 0)` → 0.

Q: What's `functools.partial` for?
A: Fix some arguments of a function: `square = partial(pow, exp=2)` → `square(5)` = 25.

Q: What does `itertools.count` do?
A: Infinite counter: `zip(count(), ['a','b'])` → `[(0,'a'), (1,'b')]`.

Q: What does `itertools.cycle` do?
A: Infinite repetition: `islice(cycle([1,2]), 5)` → `[1,2,1,2,1]`.

Q: What does `itertools.islice` do?
A: Slice an iterator: `islice(range(100), 5, 15)` → `[5..14]` without creating full list.

Q: What does `itertools.chain` do?
A: Concatenate iterables: `chain([1,2], [3,4])` → `[1,2,3,4]`. `chain.from_iterable(matrix)` flattens.

Q: Difference between `product`, `permutations`, `combinations`?
A: `product` = Cartesian product (ordered, with replacement). `permutations` = ordered, no replacement. `combinations` = unordered, no replacement.

Q: What does `itertools.groupby` require?
A: Input must be pre-sorted by the grouping key. Groups consecutive items with same key.

Q: What does `operator.itemgetter` do?
A: Returns callable extracting item by index/key: `itemgetter(1)(["a","b"])` → `"b"`. Faster than lambda.

Q: What does `operator.attrgetter` do?
A: Extracts attribute: `attrgetter("age")(person)` → `person.age`. Use with `sorted(key=)`.

Q: What does `operator.methodcaller` do?
A: Calls method by name: `methodcaller("upper")("hi")` → `"HI"`. `methodcaller("replace"," ","-")("a b")` → `"a-b"`.

Q: How to group by key using dict comprehension?
A: `{k: [v for k2,v in data if k2==k] for k in set(k for k,_ in data)}` — inefficient for large data.

Q: Better way to group — use `itertools.groupby`?
A: Sort first, then `{k: [v for _,v in g] for k,g in groupby(sorted_data, key=lambda x: x[0])}`.

Q: What's the `operator` module arithmetic functions?
A: `add(a,b)`, `mul(a,b)`, `sub(a,b)`, `truediv(a,b)` — use with `reduce`: `reduce(add, [1,2,3])` → 6.
