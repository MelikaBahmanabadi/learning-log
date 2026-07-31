# Ch 5: Functions, Scope & Closures

## Books Covered
- **Fluent Python (2nd Ed)** — Ch 6: Design Patterns with First-Class Functions, Ch 7: Function Decorators and Closures (first-class functions, closures, nonlocal, decorators)
- **Effective Python (3rd Ed)** — Items 5–8: unpacking, multiple assignment, *args/**kwargs, default arguments, *-only positional
- **Python Cookbook (3rd Ed)** — Ch 7: Functions (defaults, closures, currying, function attributes, *args/**kwargs)

## Roadmap Sections Covered
- ✅ Function definition & invocation, positional vs keyword args
- ✅ Default arguments (evaluation timing gotcha)
- ✅ `*args` / `**kwargs`, argument unpacking
- ✅ Keyword-only & positional-only parameters
- ✅ First-class functions: assign, pass, return, store
- ✅ Higher-order functions (`map`, `filter`, `sorted` key, `functools.reduce`, `partial`)
- ✅ Closures: capturing state, late-binding gotcha
- ✅ `nonlocal` and the `global` statement
- ✅ Scope: LEGB rule (Local → Enclosing → Global → Built-in)
- ✅ Lambdas
- ✅ Function attributes, introspection (`__defaults__`, `__code__`, `inspect.signature`)
- ✅ Recursion (base case, stack depth, tail-call caveat)

---

## 5.1 Function Basics

```python
# Definition & invocation
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Melika")                    # "Hello, Melika!"
greet("Ali", greeting="Hi")        # keyword — "Hi, Ali!"

# Positional vs keyword
greet("Ali", "Hey")                # positional for both
```

### Parameter Passing Model

Python uses **call-by-object-reference** (sometimes called "call by sharing"):
- Mutable objects passed in **can be mutated** inside the function
- Rebinding a parameter name does **not** affect the caller

```python
def append_item(lst, item):
    lst.append(item)      # mutates the caller's list — visible outside
    lst = [1]             # rebinding — local only, caller unaffected

a = []
append_item(a, 42)
a                          # [42]
```

### Default Arguments — The Mutable Default Gotcha

```python
def f(x, lst=[]):          # ❌ default evaluated ONCE at def time
    lst.append(x)
    return lst

f(1)    # [1]
f(2)    # [1, 2]  ← the SAME list object reused!
```

```python
def f(x, lst=None):        # ✅ idiomatic
    if lst is None:
        lst = []
    lst.append(x)
    return lst

f(1)    # [1]
f(2)    # [2]
```

**Rule:** never use a mutable default. Use `None` + check. Defaults are evaluated once, at function definition time — never use values that change (`[]`, `{}`, `datetime.now()`, `random()`).

### `*args` / `**kwargs` & Unpacking

```python
def collect(*args, **kwargs):
    # args  → tuple of positional
    # kwargs → dict of keyword
    print(args, kwargs)

collect(1, 2, x=3)           # (1, 2) {'x': 3}

# Argument unpacking (inverse)
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
add(*nums)                   # 6
d = {"a": 1, "b": 2, "c": 3}
add(**d)                     # 6
```

### Keyword-Only & Positional-Only Parameters

```python
def f(a, b, *, c):           # * separates — everything AFTER is keyword-only
    return a + b + c

f(1, 2, c=3)                 # 6
f(1, 2, 3)                   # TypeError

def f(a, b, /, c, *, d):     # / → before it positional-only
    pass

f(1, 2, 3, d=4)              # OK
f(1, 2, c=3, d=4)            # TypeError — c is positional in signature
```

**Effective Python Item 8:** keyword-only args make calls self-documenting and prevent argument-order bugs. Python 3.8+ supports positional-only with `/`.

---

## 5.2 First-Class Functions & Higher-Order Functions

In Python functions are **first-class objects**: can be assigned, passed as arguments, returned, stored in data structures.

```python
def shout(text):
    return text.upper()

speaker = shout              # assign
speaker("hi")                # "HI"

# Pass as argument
def apply(fn, x):
    return fn(x)

apply(shout, "hi")           # "HI"

# Return a function
def make_adder(n):
    def add(x):
        return x + n
    return add

add5 = make_adder(5)
add5(10)                     # 15
```

### Higher-Order Functions

```python
nums = [1, 2, 3, 4, 5]

list(map(lambda x: x * 2, nums))      # [2, 4, 6, 8, 10]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4]

# sorted with key — the workhorse
words = ["bb", "a", "ccc"]
sorted(words, key=len)                 # ['a', 'bb', 'ccc']
sorted(words, key=lambda w: w[-1])     # sort by last char

# functools
from functools import reduce, partial

reduce(lambda a, b: a + b, nums)       # 15 — cumulative
mul2 = partial(lambda a, b: a * b, 2)  # fix first arg
mul2(5)                                # 10

# operator module avoids lambdas
from operator import itemgetter, attrgetter
data = [("b", 2), ("a", 1)]
sorted(data, key=itemgetter(1))        # [('a', 1), ('b', 2)] — sort by value
```

**Fluent Python Ch 6 insight:** first-class functions make design patterns (Strategy, Command) trivial — pass a function instead of building an object hierarchy.

---

## 5.3 Lambdas

```python
# Single-expression anonymous function
square = lambda x: x ** 2     # mostly avoid naming — use def
square(5)                     # 25

# Inline use
sorted(["a2", "a10"], key=lambda s: int(s[1:]))
```

**Lambda rules:** single expression only, no statements (`return`, `assert`, `if/else` as statement). Prefer `def` when you'd name it. Useful for short `key=`/`func=` arguments.

**Late-binding gotcha:** lambdas (and closures) in a loop capture the **variable**, not the value:

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]               # [2, 2, 2] — all see final i

funcs = [lambda i=i: i for i in range(3)]  # fix: bind as default
[f() for f in funcs]               # [0, 1, 2]
```

---

## 5.4 Scope & the LEGB Rule

Names are resolved: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)          # "local"
    inner()

outer()
```

- Assignment inside a function makes the name **local** by default
- Reading a name falls back outward through LEGB
- Built-ins live in `builtins` module (last resort)

### `global` and `nonlocal`

```python
count = 0

def incr():
    global count           # rebind the module-level name
    count += 1

def outer():
    n = 0
    def inner():
        nonlocal n         # rebind the enclosing function's name
        n += 1
    inner()
    return n

outer()                    # 1
```

**Effective Python Item 21 / Fluent Ch 7:** `global` — avoid except module-level flags. `nonlocal` — needed to reassign a captured variable; prefer avoiding both by returning values when possible.

**Gotcha:** reading a global then assigning it in the same scope → `UnboundLocalError`:

```python
n = 10
def f():
    print(n)     # UnboundLocalError — n is local (assigned below)
    n = 20
```

---

## 5.5 Closures

A **closure** = a function + the non-global variables it captures from its enclosing scope, kept alive after the enclosing function returns.

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count       # captured cell
        count += 1
        return count
    return counter

c1 = make_counter()
c1()   # 1
c1()   # 2
c2 = make_counter()          # separate closure, separate count
c2()   # 1
```

**Fluent Python Ch 7:** `nonlocal` marks `count` as a free variable living in a **cell**, so the closure can rebind it across calls. Without `nonlocal`, `count += 1` would create a new local and `UnboundLocalError`.

### Late Binding & Closure Gotcha

```python
def register(handlers):
    funcs = []
    for n in range(3):
        def f():
            return n          # captures the variable n, not its value
        funcs.append(f)
    return funcs

[f() for f in register(None)]  # [2, 2, 2] — loop done, n == 2
```

Fix by binding as a default arg (`def f(n=n):`) or `functools.partial`.

---

## 5.6 Recursion

```python
def factorial(n):
    if n <= 1:                # base case — MUST exist
        return 1
    return n * factorial(n - 1)

factorial(5)                  # 120
```

- Every recursion needs a base case, or you hit `RecursionError`
- Default recursion limit: ~1000 (`sys.getrecursionlimit()`)
- Recursion in Python is limited — prefer iteration for deep cases
- For tree/graph traversal, recursion is natural and idiomatic

```python
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

---

## 5.7 Function Introspection

```python
def f(a, b=1, *args, c=2, **kwargs):
    pass

f.__name__             # 'f'
f.__defaults__         # (1,) — positional defaults
f.__kwdefaults__       # {'c': 2} — keyword-only defaults
f.__code__.co_varnames # ('a', 'b', 'args', 'c', 'kwargs')
f.__code__.co_argcount  # 2

from inspect import signature
sig = signature(f)
str(sig)               # '(a, b=1, *args, c=2, **kwargs)'
sig.parameters["a"].kind
```

**Effective Python Item 26 / Cookbook 7.1:** `inspect.signature` + `functools.wraps` are the building blocks for writing robust decorators and tools.

---

## 5.8 Practice Checklist

- [ ] Write functions with defaults, `*args`, `**kwargs`, keyword-only params
- [ ] Avoid mutable default arguments (`None` + check pattern)
- [ ] Use `map`/`filter`/`sorted(key=)`/`reduce`/`partial` as higher-order tools
- [ ] Explain LEGB scope resolution with examples
- [ ] Use `global`/`nonlocal` correctly (prefer avoiding)
- [ ] Build a closure that keeps state across calls
- [ ] Fix the late-binding gotcha (loop closures)
- [ ] Write recursive functions with base cases

---

## Flashcards

See: [flashcards.md](../flashcards.md), [flashcards-fa.md](../flashcards-fa.md)

## Progress

- [ ] Read Fluent Python Ch 6–7 — First-Class Functions, Decorators & Closures
- [ ] Read Effective Python Items 5–8 — functions, args, defaults
- [ ] Read Python Cookbook Ch 7 — Functions
- [ ] Practice: closures, nonlocal, default args, higher-order functions
- [ ] Implement a stateful closure and a decorator that keeps state
