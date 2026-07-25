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
