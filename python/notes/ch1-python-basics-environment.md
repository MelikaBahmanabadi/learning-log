# Ch 1: Python Basics & Environment

## Books Covered
- **Fluent Python (2nd Ed)** — Ch 1: The Python Data Model (intro)
- **Effective Python (3rd Ed)** — Items 1–4: Thinking in Python
- **Clean Code** — Ch 2–3: Meaningful Names, Functions
- **Python Cookbook (3rd Ed)** — Ch 1: Data Structures & Algorithms (basics)
- **Cracking the Coding Interview** — Ch 1: Basics (foundational mindset)

## Roadmap Sections Covered
- ✅ Installation & Environment
- ✅ Variables & Data Types
- ✅ Operators
- ✅ Input & Output
- ✅ Conditional Statements
- ✅ Loops
- ✅ Functions
- ✅ Modules & Packages
- ✅ File Handling
- ✅ Exception Handling (intro — deep dive in Ch 21)
- ✅ Collections (list, tuple, set, dict)
- ✅ String Manipulation
- ✅ List/Dict/Set Comprehensions
- ✅ Basic Coding Best Practices

---

## 1.1 Installation & Environment

### Python Versions
- Python 3.11+ recommended (3.12+ for latest features)
- **CPython** — reference implementation (what you download from python.org)
- **PyPy** — JIT-compiled, faster for pure Python loops
- **Anaconda** — distribution with data science packages pre-installed
- **Miniconda** — minimal conda, install only what you need

### Virtual Environments

```bash
# Built-in venv (recommended for most projects)
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
deactivate

# Conda environments (data science / ML projects)
conda create -n ml-env python=3.12
conda activate ml-env
conda deactivate

# uv — ultra-fast package manager (Rust-based)
uv venv
uv pip install requests
```

### pyproject.toml (Modern Standard, PEP 517/518/621)

```toml
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-project"
version = "0.1.0"
description = "My Python project"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.28",
    "numpy>=1.26",
]

[project.optional-dependencies]
dev = ["pytest>=7", "ruff>=0.1", "mypy>=1.0"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
strict = true
```

### Python Version Management

```bash
# pyenv — install multiple Python versions
pyenv install 3.12.0
pyenv global 3.12.0   # system-wide default
pyenv local 3.11.6    # per-project (creates .python-version)

# conda — environment + version management
conda create -n py311 python=3.11
```

### Recommended Dev Tools

| Tool | Purpose | Install |
|------|---------|---------|
| **ruff** | Linter + formatter | `pip install ruff` |
| **mypy** | Static type checker | `pip install mypy` |
| **pytest** | Testing framework | `pip install pytest` |
| **ipython** | Interactive REPL | `pip install ipython` |
| **jupyter** | Notebooks for data science | `pip install jupyter` |
| **pre-commit** | Git hooks | `pip install pre-commit` |

```bash
# Quick start dev setup
mkdir my_project && cd my_project
python -m venv .venv
source .venv/bin/activate
pip install ruff mypy pytest pre-commit
ruff init  # generates ruff config
```

---

## 1.2 Variables & Data Types

### Dynamic Typing

Python is **dynamically typed** — variables don't declare their type; the value has a type.

```python
x = 5           # int
x = "hello"     # now str — no error
```

**Strongly typed** — implicit type coercion is rare:

```python
5 + "3"   # TypeError: unsupported operand type(s)
5 + 3     # 8 (int)
"5" + "3" # "53" (str)
```

### Basic Types

| Type | Category | Example | Mutable? |
|------|----------|---------|----------|
| `int` | Numeric | `42`, `-5`, `10**100` | No |
| `float` | Numeric | `3.14`, `1e-5`, `inf`, `nan` | No |
| `complex` | Numeric | `3+4j`, `complex(1, 2)` | No |
| `bool` | Boolean | `True`, `False` | No (subclass of int) |
| `str` | Text | `"hello"`, `f"val={x}"` | No |
| `bytes` | Binary | `b"hello"`, `bytes([65, 66])` | No |
| `list` | Sequence | `[1, 2, 3]` | Yes |
| `tuple` | Sequence | `(1, 2, 3)` | No |
| `range` | Sequence | `range(10)` | No |
| `dict` | Mapping | `{"a": 1, "b": 2}` | Yes |
| `set` | Set | `{1, 2, 3}` | Yes |
| `frozenset` | Set | `frozenset([1, 2])` | No |
| `NoneType` | Null | `None` | No |

### Type Conversion

```python
int("42")        # 42
float("3.14")    # 3.14
str(42)          # "42"
bool(1)          # True
bool(0)          # False
bool("")         # False
bool([])         # False
list("abc")      # ["a", "b", "c"]
tuple([1, 2])    # (1, 2)
set([1, 2, 2])   # {1, 2}
```

### Truthiness Check

Every object in Python has a truth value:

| Truthy ✅ | Falsy ❌ |
|-----------|---------|
| Non-zero numbers | `0`, `0.0`, `0j` |
| Non-empty sequences | `""`, `[]`, `()`, `{}`, `set()` |
| `True` | `False` |
| Objects (by default) | `None` |

```python
if x:           # Pythonic — truthiness check
    ...

if len(x) > 0:  # Unpythonic — don't do this
    ...
```

### Variables & Assignment

```python
# Multiple assignment
a, b, c = 1, 2, 3

# Swapping (Pythonic)
a, b = b, a

# Unpacking
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5

# Ignoring values with _
_, b, _ = (1, 2, 3)  # b = 2

# Chained assignment
a = b = c = 0
```

### Variable Naming (PEP 8)

| Construct | Convention | Example |
|-----------|-----------|---------|
| Variable | `snake_case` | `user_name` |
| Constant | `UPPER_SNAKE` | `MAX_RETRIES` |
| Private | `_leading_underscore` | `_internal_id` |
| Name-mangled | `__double_underscore` | `__private_attr` |
| Built-in conflict | `trailing_` | `class_` |

### Clean Code Naming Principles (Clean Code Ch 2)

| Principle | Good ✅ | Bad ❌ |
|-----------|---------|-------|
| Intention-revealing | `elapsed_time_in_days` | `d` |
| Pronounceable | `generation_timestamp` | `gen_ts` |
| Searchable | `MAX_RETRIES = 5` | magic number `5` |
| Avoid disinformation | `customers_list` | `customer_lst` |
| One word per concept | always `fetch` | mix `fetch/get/retrieve` |
| Don't add gratuitous context | `name` (in Customer class) | `customer_name` (in Customer class) |

---

## 1.3 Operators

### Arithmetic

```python
+  -  *  /       # add, subtract, multiply, divide (always returns float)
//               # floor division (integer division)
%                # modulo (remainder)
**               # exponentiation (power)
```

```python
7 / 3      # 2.333... (float)
7 // 3     # 2 (floor division)
7 % 3      # 1 (modulo)
-7 // 3    # -3 (floor — goes DOWN)
7 ** 3     # 343
```

### Comparison

```python
==  !=  <  >  <=  >=    # standard comparisons
is  is not               # identity (object equality, not value)
in  not in               # membership
```

```python
a == b    # value equality
a is b    # same object in memory (use for None: x is None)

# Chained comparison (Pythonic)
0 < x < 10               # True if x between 0 and 10 (exclusive)
x == y == z              # True if all equal
```

### Logical

```python
and   or   not    # short-circuit operators
```

```python
True and False    # False
True or False     # True
not True          # False

# Short-circuit: Python stops evaluating as soon as result is known
def get_user():
    print("get_user called")
    return None

user = get_user() or "guest"  # "guest" — get_user returns falsy None
```

### Assignment Operators

```python
=   +=   -=   *=   /=   //=   %=   **=
&=   |=   ^=   >>=   <<=
```

```python
x = 10
x += 5   # x = 15
x *= 2   # x = 30
```

### Walrus Operator `:=` (Python 3.8+)

```python
# Assignment expression — assign AND use in expression

# Without walrus
data = get_data()
if data:
    process(data)

# With walrus ✅
if (data := get_data()):
    process(data)

# In while loops
while (chunk := file.read(1024)):
    process(chunk)
```

**Use sparingly** — only when it makes code more readable, not less.

---

## 1.4 Input & Output

### print() Basics

```python
print("hello")              # hello\n
print("hello", "world")    # hello world (space separator)
print("hello", end="")     # no newline
print("a", "b", sep=",")   # a,b

# f-strings (Python 3.6+)
name = "Melika"
age = 25
print(f"{name} is {age} years old")        # Melika is 25 years old
print(f"{name!r} is {age}")                # 'Melika' is 25 (repr)
print(f"pi = {3.14159:.2f}")              # pi = 3.14
print(f"{age:04d}")                         # 0025 (zero-padded)
print(f"{100000:,}")                        # 100,000 (comma separator)
```

### input()

```python
name = input("Enter your name: ")   # always returns str
age = int(input("Enter age: "))     # convert to int
```

### Formatted String Literals (f-strings Deep)

```python
# Expressions inside f-strings
f"{2 * 3}"                              # "6"
f"{[x**2 for x in range(5)]}"           # "[0, 1, 4, 9, 16]"
f"{func()}"                             # result of func call

# Format specifiers
f"{value:10}"        # width=10
f"{value:<10}"       # left-align
f"{value:>10}"       # right-align
f"{value:^10}"       # center
f"{value:010}"       # zero-pad width=10
f"{value:+}"         # always show sign
f"{value:.3f}"       # 3 decimal places
f"{value:.2e}"       # scientific notation
f"{value:%}"         # percentage
f"{value:,.2f}"      # comma + 2 decimals

# Date formatting
from datetime import datetime
now = datetime.now()
f"{now:%Y-%m-%d %H:%M}"   # "2026-07-25 15:30"
```

### Old-style formatting (know for legacy code)

```python
"%s is %d years old" % (name, age)    # %-formatting
"{} is {} years old".format(name, age) # str.format()
```

---

## 1.5 Conditional Statements

### if / elif / else

```python
if condition:
    pass
elif other_condition:
    pass
else:
    pass
```

### Conditional Expression (Ternary)

```python
age = 20
status = "adult" if age >= 18 else "minor"

# Nested ternary — avoid, hard to read
result = "A" if score >= 90 else "B" if score >= 80 else "C"
```

### Truthiness in Conditionals

```python
# Pythonic ✅
if items:        # check non-empty
if user:         # check not None
if count:        # check non-zero

# Unpythonic ❌
if len(items) > 0:
if user is not None:
if count != 0:
```

### match/case (Python 3.10+)

```python
# Structural pattern matching
def handle_command(command):
    match command.split():
        case ["quit"]:
            sys.exit(0)
        case ["hello", name]:
            print(f"Hello, {name}!")
        case ["load", filename] if filename.endswith(".json"):
            data = json.load(open(filename))
        case _:
            print("Unknown command")
```

### Code Smell: Deep Nesting

```python
# Bad ❌ — deep nesting
if user:
    if user.is_active:
        if user.has_permission("read"):
            data = fetch_data()
            if data:
                process(data)

# Better ✅ — early returns
if not user:
    return
if not user.is_active:
    return
if not user.has_permission("read"):
    return
data = fetch_data()
if not data:
    return
process(data)
```

Also known as the **Guard Clause** pattern.

---

## 1.6 Loops

### for Loop

```python
# Iterate over sequence
for item in items:
    print(item)

# With index
for i, item in enumerate(items):
    print(i, item)

# With start index
for i, item in enumerate(items, start=1):
    print(i, item)

# Range
for i in range(10):          # 0..9
for i in range(5, 10):       # 5..9
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8

# Reverse
for item in reversed(items):
    print(item)

# Multiple sequences
for a, b in zip(xs, ys):
    print(a, b)

# Zip with index
for i, (a, b) in enumerate(zip(xs, ys)):
    print(i, a, b)

# Iterate dict
for key in d:                       # keys
for key, value in d.items():        # key-value pairs
for value in d.values():            # values
```

### while Loop

```python
while condition:
    # body

while (chunk := file.read(1024)):   # walrus + while
    process(chunk)

# Infinite loop with break
while True:
    cmd = input("> ")
    if cmd == "quit":
        break
    process(cmd)
```

### break, continue, else on loops

```python
# break — exit loop immediately
for item in items:
    if condition:
        break

# continue — skip to next iteration
for item in items:
    if skip_condition:
        continue
    process(item)

# else — runs if loop completed WITHOUT break (useful for search)
for item in items:
    if item == target:
        print("Found!")
        break
else:
    print("Not found")  # runs only if no break occurred
```

### Loop Best Practices

```python
# Bad ❌
for i in range(len(items)):
    print(items[i])

# Good ✅
for item in items:
    print(item)

# Bad ❌ — modifying list while iterating
for item in items:
    if condition(item):
        items.remove(item)

# Good ✅ — iterate copy
for item in items.copy():
    if condition(item):
        items.remove(item)

# Better ✅ — list comprehension
items = [item for item in items if not condition(item)]
```

---

## 1.7 Functions

### Defining & Calling

```python
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting message."""
    return f"{greeting}, {name}!"

# Positional
greet("Melika")

# Keyword
greet(name="Melika", greeting="Hi")

# Default argument — MUTABLE DEFAULT GOTCHA
def add_item(item, lst=[]):     # ❌ BAD — list is shared across calls
    lst.append(item)
    return lst

add_item(1)  # [1]
add_item(2)  # [1, 2] — not [2]!

def add_item(item, lst=None):   # ✅ GOOD
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Argument Types

```python
# Positional-only (Python 3.8+)
def div(a, b, /):
    return a / b

div(10, 2)      # ✅
div(a=10, b=2)  # ❌ TypeError

# Keyword-only
def safe_div(a, b, *, allow_zero=False):
    if not allow_zero and b == 0:
        raise ValueError("Division by zero")
    return a / b

safe_div(10, 2)                    # ✅
safe_div(10, 2, allow_zero=False)  # ✅
safe_div(10, 2, False)             # ❌ TypeError (must be keyword)

# Combined
def func(pos_only, /, pos_or_kwd, *, kwd_only):
    pass
```

### *args and **kwargs

```python
def log(message, *args, **kwargs):
    """Accepts variable positional and keyword arguments."""
    print(f"[LOG] {message}")
    if args:
        print(f"  positional: {args}")
    if kwargs:
        print(f"  keyword: {kwargs}")

log("Start")                         # [LOG] Start
log("Values", 1, 2, 3)              # [LOG] Values  positional: (1, 2, 3)
log("Config", user="melika", role="admin")

# Unpacking for forwarding
def wrapper(*args, **kwargs):
    return target(*args, **kwargs)   # passes through unchanged
```

### Return Values

```python
# Single return
def square(x):
    return x * x

# Multiple values (tuple)
def min_max(items):
    return min(items), max(items)

low, high = min_max([3, 1, 4, 1, 5])

# Early return for guard clauses
def process_user(user):
    if not user:
        return None
    if not user.is_active:
        return None
    return compute(user)
```

### First-Class Functions

```python
# Functions are objects — assign, pass, return
def double(x):
    return x * 2

f = double            # assign to variable
f(5)                  # 10

map(double, [1, 2, 3])  # pass as argument

def make_multiplier(n):
    def multiplier(x):  # function returning function
        return x * n
    return multiplier

times2 = make_multiplier(2)
times2(5)             # 10
```

### Lambda (Anonymous Functions)

```python
lambda x: x * 2                              # single expression
lambda x, y: x + y

# Common use — key functions
sorted(items, key=lambda x: x[1])
max(items, key=lambda item: item.price)
```

**When to use lambda**: trivial single-expression operations. For anything complex, use `def`.

### Function Annotations (Type Hints)

```python
def process(users: list[str], max_count: int = 100) -> list[str]:
    """Process user names up to max_count."""
    return [u.upper() for u in users[:max_count]]

# Complex types
from typing import Optional, Union, Callable, Any

def handler(event: dict[str, Any], callback: Callable[[int], None]) -> Optional[str]:
    ...
```

---

## 1.8 Modules & Packages

### Modules (Single .py file)

```python
# mymodule.py
def greet(name):
    return f"Hello, {name}"

PI = 3.14159

# Importing
import mymodule                         # mymodule.greet("Melika")
from mymodule import greet, PI         # greet("Melika")
from mymodule import *                  # avoid — pollutes namespace
```

### Packages (Directory of modules)

```
mypackage/
├── __init__.py          # makes directory a package; can have init code
├── module_a.py
└── subpackage/
    ├── __init__.py
    └── module_b.py
```

```python
from mypackage import module_a
from mypackage.subpackage import module_b
from mypackage.module_a import some_function
```

### `__init__.py` Patterns

```python
# __init__.py — control what's exported
from .module_a import some_function
from .subpackage import important_class

__all__ = ["some_function", "important_class"]  # controls `from package import *`
```

### Import Best Practices

```python
# Order: standard library → third-party → local
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

from mypackage import mymodule
```

### `if __name__ == "__main__"` pattern

```python
# mymodule.py — can be imported OR run as script
def main():
    """Entry point when run directly."""
    args = parse_args()
    result = process(args)
    print(result)

if __name__ == "__main__":
    main()
```

### Relative Imports

```python
# Inside a package
from . import sibling      # sibling module
from .. import parent      # parent package
from .sub import thing     # submodule
```

---

## 1.9 File Handling

### The Pythonic Way: Context Manager

```python
# ✅ Pythonic — auto-closes even on exception
with open("data.txt", "r") as fh:
    data = fh.read()

# ❌ Anti-pattern — must manually close
fh = open("data.txt", "r")
data = fh.read()
fh.close()              # skipped if exception above
```

### Modes

| Mode | Description | File position |
|------|-------------|---------------|
| `"r"` | Read (default) | Start |
| `"w"` | Write (truncate) | Start |
| `"a"` | Append | End |
| `"x"` | Exclusive create (fail if exists) | Start |
| `"rb"` | Read binary | Start |
| `"wb"` | Write binary (truncate) | Start |
| `"r+"` | Read + write | Start |
| `"w+"` | Read + write (truncate) | Start |
| `"a+"` | Read + append | End |

### Reading Files

```python
# Read entire file (small files)
with open("data.txt") as fh:
    content = fh.read()           # single str

# Read lines
with open("data.txt") as fh:
    lines = fh.readlines()        # list of str (with \n)

# Iterate line by line (memory efficient for large files)
with open("data.txt") as fh:
    for line in fh:
        print(line.rstrip())      # strip trailing \n
```

### Writing Files

```python
with open("output.txt", "w") as fh:
    fh.write("hello\n")
    fh.writelines(["line1\n", "line2\n"])
```

### File Paths

```python
from pathlib import Path  # modern, cross-platform

path = Path("/Users/melika/data")
path / "subfolder" / "file.txt"   # path joining with /

path.exists()       # bool
path.is_file()
path.is_dir()
path.name           # "file.txt"
path.stem           # "file"
path.suffix         # ".txt"
path.parent         # Path("/Users/melika/data/subfolder")
path.read_text()    # read file content
path.write_text("hello")  # write file content
```

### tempfile

```python
import tempfile

# Temporary file (auto-deleted)
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as tf:
    tf.write("temporary data")
    temp_path = tf.name

# Temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    path = Path(tmpdir) / "work.txt"
    path.write_text("data")
```

---

## 1.10 Exception Handling (Intro)

### try / except / else / finally

```python
try:
    file = open("data.txt")
    data = file.read()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
except Exception as e:      # catch-all (use sparingly)
    print(f"Unexpected error: {e}")
else:
    print(f"Read {len(data)} chars")  # runs if NO exception
finally:
    file.close()                      # ALWAYS runs
```

### Common Built-in Exceptions

| Exception | When |
|-----------|------|
| `ValueError` | Wrong value (e.g., `int("abc")`) |
| `TypeError` | Wrong type (e.g., `5 + "a"`) |
| `KeyError` | Missing dict key |
| `IndexError` | Index out of range |
| `AttributeError` | Missing attribute |
| `FileNotFoundError` | File doesn't exist |
| `ZeroDivisionError` | Division by zero |
| `StopIteration` | Iterator exhausted |

### Raise Your Own

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### EAFP vs LBYL

```python
# LBYL (Look Before You Leap) — common in C/Java
if os.path.exists(path):
    with open(path) as fh:
        data = fh.read()

# EAFP (Easier to Ask Forgiveness than Permission) — Pythonic ✅
try:
    with open(path) as fh:
        data = fh.read()
except FileNotFoundError:
    print("File not found")
```

EAFP wins because:
- Avoids TOCTOU race conditions
- Faster when common case succeeds
- Happy path stays unindented

---

## 1.11 Collections (list, tuple, set, dict)

### List

```python
# Creation
nums = [1, 2, 3]
mixed = [1, "a", 3.14]
zeros = [0] * 5              # [0, 0, 0, 0, 0]

# Indexing
nums[0]        # 1
nums[-1]       # 3 (last)
nums[1:3]      # [2, 3] (slice)

# Common operations
nums.append(4)          # [1, 2, 3, 4] — O(1)
nums.extend([5, 6])     # [1, 2, 3, 4, 5, 6]
nums.insert(0, 0)       # [0, 1, 2, 3, ...] — O(n)
nums.pop()              # removes & returns last — O(1)
nums.pop(0)             # removes & returns first — O(n)
nums.remove(3)          # removes first occurrence of 3 — O(n)
3 in nums               # True / False — O(n)
nums.index(3)           # index of first 3 — O(n)
nums.sort()             # in-place sort — O(n log n)
sorted(nums)            # returns new sorted list
nums.reverse()
list(reversed(nums))
```

### Tuple

```python
# Immutable sequence
point = (3, 4)
single = (1,)           # trailing comma required!
empty = ()              # empty tuple

# Named access
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p.y                # named access
x, y = p                # unpacking
```

### Set

```python
# Unordered collection of unique elements
colors = {"red", "green", "blue"}
unique = set([1, 2, 2, 3])  # {1, 2, 3}

# Operations
colors.add("yellow")     # add element
colors.discard("red")    # remove if exists (no error)
colors.remove("red")     # remove (raises KeyError if missing)

# Set algebra
a = {1, 2, 3}
b = {2, 3, 4}
a | b   # {1, 2, 3, 4}  — union
a & b   # {2, 3}        — intersection
a - b   # {1}           — difference
a ^ b   # {1, 4}        — symmetric difference
a <= b  # False         — subset
a >= b  # False         — superset
```

### Dict

```python
# Key-value mapping
user = {"name": "Melika", "age": 25}

# Access
user["name"]            # "Melika"
user.get("name")        # "Melika"
user.get("country")     # None (no error)
user.get("country", "Unknown")  # "Unknown" (default)
user.setdefault("role", "user")  # set if missing, return value

# Check
"name" in user           # True — Pythonic ✅

# Update
user["age"] = 26
user.update({"role": "admin"})

# Delete
del user["age"]
user.pop("role")         # returns value, raises KeyError if missing
user.pop("role", None)   # safe pop with default

# Keys, values, items
list(user.keys())        # keys view
list(user.values())      # values view
list(user.items())       # (key, value) pairs

# Merging (Python 3.9+)
combined = user | other_dict
user |= other_dict       # in-place
```

---

## 1.12 String Manipulation

### Common Methods

```python
s = "  Hello, World!  "

# Case
s.upper()           # "  HELLO, WORLD!  "
s.lower()           # "  hello, world!  "
s.capitalize()      # "  hello, world!  "
s.title()           # "  Hello, World!  "
s.swapcase()        # "  hELLO, wORLD!  "

# Trimming
s.strip()           # "Hello, World!"
s.lstrip()          # "Hello, World!  "
s.rstrip()          # "  Hello, World!"

# Searching
s.find("World")     # 7 (index, -1 if not found)
s.index("World")    # 7 (raises ValueError if not found)
s.count("o")        # 2
"World" in s        # True

# Checking
s.isdigit()         # False
s.isalpha()         # False
s.isalnum()         # False
s.startswith("  He")  # True
s.endswith("!")       # True

# Splitting & Joining
s.split(",")        # ["  Hello", " World!  "]
s.split()           # ["Hello,", "World!"]  (whitespace)
" ".join(["a", "b", "c"])  # "a b c"  (join is STR method)

# Replacement
s.replace("Hello", "Hi")  # "  Hi, World!  "
s.strip().replace("World", "Python")  # "Hello, Python!"
```

### f-strings for Formatting

```python
name = "Melika"
score = 85.5

f"Name: {name:10} Score: {score:.1f}"
# "Name: Melika     Score: 85.5"
```

### Raw Strings

```python
path = r"C:\Users\name"   # raw — no escape sequences
regex = r"\d+\.\d+"       # raw for regex patterns
```

### Multiline Strings

```python
text = """
This is a
multiline
string.
"""
```

---

## 1.13 List/Dict/Set Comprehensions

### List Comprehension

```python
# Basic: [expr for item in iterable if condition]
squares = [x**2 for x in range(10)]           # [0, 1, 4, 9, ..., 81]
evens = [x for x in range(20) if x % 2 == 0]  # [0, 2, 4, ..., 18]

# Nested comprehension (flatten)
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]     # [1, 2, 3, 4, 5, 6]

# With if-else (ternary in comprehension)
tags = ["good" if score > 80 else "needs work" for score in scores]

# Comprehension vs map/filter
[x*2 for x in items]              # ✅ more readable
list(map(lambda x: x*2, items))    # ❌ prefer comprehension
```

### Dict Comprehension

```python
squares = {x: x**2 for x in range(5)}      # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Filter + transform
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}

# Invert dict
inverted = {v: k for k, v in original.items()}
```

### Set Comprehension

```python
unique_lens = {len(word) for word in words}   # {3, 5, 7, ...}
evens_set = {x for x in range(20) if x % 2 == 0}
```

### When NOT to use comprehensions

```python
# ❌ Too complex — use a for loop
result = [
    process(transform(item))
    for item in items
    if condition1(item)
    if condition2(item)
    for sub in item.subs
    if sub.qualifies()
]

# ✅ Better as loop
result = []
for item in items:
    if condition1(item) and condition2(item):
        for sub in item.subs:
            if sub.qualifies():
                result.append(process(transform(item)))
```

**Rule of thumb**: if a comprehension spans more than 2 lines, use a loop.

---

## 1.14 Basic Coding Best Practices

### PEP 8 Quick Reference

| Rule | Good ✅ | Bad ❌ |
|------|---------|-------|
| 4 spaces per indent | `····return` | `\treturn` |
| 88 chars max (black default) | — | — |
| Two blank lines around top-level defs | — | — |
| One blank line around method defs | — | — |
| Spaces around operators | `x = y + 3` | `x=y+3` |
| No spaces around `=` in defaults | `def f(x=5)` | `def f(x = 5)` |

### The Zen of Python (PEP 20)

```python
import this  # print the Zen
```

Key excerpts:
- **Beautiful is better than ugly.**
- **Explicit is better than implicit.**
- **Simple is better than complex.**
- **Flat is better than nested.**
- **Readability counts.**
- There should be one — and preferably only one — obvious way to do it.

### Code Smells to Avoid

```python
# 1. Magic numbers ❌
if status == 3:  ...

# 2. ✅ Named constants
STATUS_ACTIVE = 3
if status == STATUS_ACTIVE: ...

# 3. Long functions — split into smaller ones
# 4. Deep nesting — guard clauses
# 5. Unused variables / imports
# 6. Mutable default arguments (covered above)
# 7. Comparing to True/False/None directly
if x == True: ...    # ❌
if x: ...            # ✅
if x is None: ...    # ✅ (identity for None)
```

### Simple is Better Than Complex

```python
# ❌ Overly clever
result = [y for x in range(10) if (y := x * 2) > 5]

# ✅ Clear
result = []
for x in range(10):
    y = x * 2
    if y > 5:
        result.append(y)
```

---

## 1.15 Practice Checklist

- [ ] Set up Python 3.12 + virtual environment
- [ ] Write a script with functions, if/else, loops
- [ ] Read and write files using `with` statement
- [ ] Use list/dict/set comprehensions
- [ ] Handle exceptions with try/except
- [ ] Create a module and import it
- [ ] Write f-strings with format specifiers
- [ ] Use `pathlib.Path` for file operations

---

## Flashcards

See: [flashcards.md](../flashcards.md), [flashcards-fa.md](../flashcards-fa.md)

## Progress

- [ ] Read Effective Python Items 1–4
- [ ] Read Clean Code Ch 2–3
- [ ] Practice: file I/O, comprehensions, functions, error handling
- [ ] Set up dev environment: venv + pyproject.toml + ruff/mypy
