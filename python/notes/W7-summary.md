# Ch 7: Modules, Packages & Import System

## Books Covered
- **Python Cookbook (3rd Ed)** — Ch 7: Modules & Packages (importing, packages, namespace packages, `__init__.py`, relative imports, `importlib`, `pkgutil`, `runpy`)
- **Effective Python (3rd Ed)** — Items related to modules/packages
- **Fluent Python (2nd Ed)** — Relevant sections on modules

## Roadmap Sections Covered
- ✅ Module basics: `.py` files, `import` statement
- ✅ Package structure: `__init__.py`, submodules
- ✅ Absolute vs relative imports
- ✅ `__init__.py` patterns: explicit exports, lazy imports
- ✅ Namespace packages (PEP 420)
- ✅ `importlib` — dynamic imports, `import_module`, `reload`
- ✅ `pkgutil` / `importlib.resources` — package data access
- ✅ `runpy` — run modules as scripts
- ✅ `__name__ == "__main__"` pattern
- ✅ Virtual environments & `sys.path`
- ✅ `pyproject.toml` and modern packaging

---

## 7.1 Module Basics

A **module** is a `.py` file containing Python definitions and statements. The module name is the filename without `.py`.

```python
# math_utils.py
PI = 3.14159

def circle_area(radius):
    return PI * radius ** 2

def circle_circumference(radius):
    return 2 * PI * radius
```

### Importing

```python
# Import entire module
import math_utils
math_utils.circle_area(5)

# Import specific names
from math_utils import circle_area, PI
circle_area(5)

# Import with alias
import math_utils as mu
mu.circle_area(5)

# Import all (use sparingly)
from math_utils import *  # imports everything not starting with _
```

### Module Execution & `__name__`

When a module is imported, its code runs **once**. The special variable `__name__`:
- `"__main__"` when run directly: `python math_utils.py`
- Module name when imported: `"math_utils"`

```python
# math_utils.py
def circle_area(radius):
    return 3.14159 * radius ** 2

if __name__ == "__main__":           # Only runs when executed directly
    print(circle_area(5))            # Test/demo code
```

---

## 7.2 Packages

A **package** is a directory containing an `__init__.py` file (or a namespace package without it) and modules/subpackages.

```
myproject/
├── main.py
└── mypackage/
    ├── __init__.py
    ├── module_a.py
    └── subpackage/
        ├── __init__.py
        └── module_b.py
```

### `__init__.py` — Package Initialization

Runs when package or any submodule is first imported. Controls what's exported.

```python
# mypackage/__init__.py

# Explicit exports — defines public API
from .module_a import func_a
from .subpackage.module_b import func_b

__all__ = ["func_a", "func_b"]  # Controls `from mypackage import *`

# Package-level constants
VERSION = "1.0.0"

# Lazy imports — defer heavy imports until needed
# def __getattr__(name):  # Python 3.7+
#     if name == "heavy_module":
#         from . import heavy_module
#         return heavy_module
#     raise AttributeError(name)
```

### Submodule Imports

```python
# main.py
import mypackage.module_a
from mypackage.subpackage import module_b

# Or import from package namespace (if exposed in __init__.py)
from mypackage import func_a, func_b
```

---

## 7.3 Absolute vs Relative Imports

### Absolute Imports (Preferred)

Full path from project root — clear, unambiguous.

```python
# In mypackage/subpackage/module_b.py
from mypackage.module_a import func_a     # Absolute from project root
import mypackage.module_a                 # Also absolute
```

### Relative Imports

Use `.` for current package, `..` for parent package. Only work **inside packages**.

```python
# In mypackage/subpackage/module_b.py
from . import module_c           # Same package (mypackage.subpackage.module_c)
from ..module_a import func_a    # Parent package (mypackage.module_a)
from .. import something         # Parent package
```

**Rules:**
- Relative imports only work when module is **part of a package** (has `__package__`)
- Cannot use relative imports in scripts run directly (`__main__`)
- Absolute imports are generally preferred for clarity

---

## 7.4 Namespace Packages (PEP 420)

Packages **without** `__init__.py` — multiple directories contribute to the same namespace.

```
# Directory structure (no __init__.py in namespace_pkg)
site-packages/
├── namespace_pkg/
│   └── part_a/
│       └── module_a.py
└── namespace_pkg/
    └── part_b/
        └── module_b.py
```

```python
# Both work — merged into single namespace_pkg
from namespace_pkg.part_a import module_a
from namespace_pkg.part_b import module_b
```

**Use cases:** Large projects split across multiple distributions, plugins.

---

## 7.5 `importlib` — Dynamic Imports

Programmatic import control.

### `importlib.import_module(name, package=None)`

```python
import importlib

# Dynamic import by string name
mod = importlib.import_module("json")
mod.dumps({"a": 1})              # '{"a": 1}'

# Relative import programmatically
mod = importlib.import_module(".module_a", package="mypackage")
```

### `importlib.reload(module)`

Reload a previously imported module — useful for development.

```python
import mymodule
import importlib

# After editing mymodule.py...
importlib.reload(mymodule)       # Re-executes module code
```

### `importlib.util` — Loader/Finders

```python
import importlib.util

# Load module from file path
spec = importlib.util.spec_from_file_location("mymod", "/path/to/mymod.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.some_function()
```

---

## 7.6 Package Data & Resources

### `importlib.resources` (Python 3.7+) — Recommended

Read data files bundled with packages.

```
mypackage/
├── __init__.py
├── data/
│   └── config.json
└── module.py
```

```python
# module.py
from importlib.resources import files, as_file

# Read as text (preferred)
data = files("mypackage.data").joinpath("config.json").read_text()

# Or as binary
data = files("mypackage.data").joinpath("config.json").read_bytes()

# For paths needing filesystem access (e.g., C libraries)
with as_file(files("mypackage.data").joinpath("config.json")) as path:
    load_c_library(path)
```

### `pkgutil` — Legacy but Still Useful

```python
import pkgutil

# Get package data as bytes
data = pkgutil.get_data("mypackage", "data/config.json")
# b'{"key": "value"}'

# Iterate over modules in package
for importer, modname, ispkg in pkgutil.iter_modules(mypackage.__path__):
    print(modname, ispkg)
```

---

## 7.7 `runpy` — Run Modules as Scripts

```python
import runpy

# Run module as __main__ (like `python -m mymodule`)
runpy.run_module("mymodule", run_name="__main__")

# Run .py file as __main__
runpy.run_path("/path/to/script.py", run_name="__main__")
```

**Use cases:** Test runners, plugin systems, executing user code.

---

## 7.8 `sys.path` & Module Search

Python searches for modules in `sys.path`:
1. Directory of the script being run (or `''` for current dir)
2. `PYTHONPATH` environment variable
3. Standard library paths
4. `site-packages` (installed packages)

```python
import sys

# Add to path at runtime
sys.path.insert(0, "/custom/path")

# Inspect
print(sys.path)
```

**Best practice:** Use virtual environments and proper packaging (`pip install -e .`) instead of manipulating `sys.path`.

---

## 7.9 Virtual Environments & Packaging

### Virtual Environment

```bash
# Create
python -m venv .venv

# Activate
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# Deactivate
deactivate
```

### Modern Packaging — `pyproject.toml`

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "1.0.0"
description = "My awesome package"
readme = "README.md"
authors = [{name = "You", email = "you@example.com"}]
license = {text = "MIT"}
requires-python = ">=3.9"
dependencies = [
    "requests>=2.28",
]

[project.optional-dependencies]
dev = ["pytest", "black", "ruff"]

[tool.setuptools.packages.find]
where = ["src"]          # or use find: directive
```

```bash
# Install in editable mode
pip install -e .

# Build distribution
pip build
```

---

## 7.10 Common Patterns & Gotchas

### Circular Imports

```python
# a.py
from b import func_b
def func_a(): ...

# b.py
from a import func_a    # Circular!
def func_b(): ...
```

**Fixes:**
- Move imports inside functions (lazy import)
- Restructure to avoid circular dependency
- Use `importlib` for dynamic loading

### Shadowing Standard Library

```python
# Don't name your file json.py, random.py, etc.!
# Creates import confusion
```

### `__all__` in Modules

```python
# mymodule.py
def public_func():
    pass

def _private_func():     # Leading underscore = internal
    pass

__all__ = ["public_func"]  # Controls `from mymodule import *`
```

### Conditional Imports

```python
# Optional dependency
try:
    import ujson as json
except ImportError:
    import json
```

---

## 7.11 Interview Q&A

**Q: What's the difference between a module and a package?**
A: A module is a single `.py` file. A package is a directory with `__init__.py` (or namespace package) containing modules/subpackages.

**Q: When does `__init__.py` run?**
A: When the package or any submodule is **first imported**. Runs once per interpreter session.

**Q: What does `__all__` do?**
A: Defines the public API for `from package import *`. Also documents intended exports.

**Q: Absolute vs relative imports — which to prefer?**
A: Absolute imports (PEP 8). Clearer, work everywhere. Relative imports only inside packages.

**Q: How do you fix a circular import?**
A: Move import inside function (lazy), restructure code, or use `importlib.import_module()`.

**Q: What's a namespace package (PEP 420)?**
A: Package without `__init__.py` — multiple directories merge into one namespace. Used for plugins, split distributions.

**Q: How to read a data file bundled with a package?**
A: `importlib.resources.files("pkg.data").joinpath("file.json").read_text()` (Python 3.7+).

**Q: What does `importlib.reload()` do?**
A: Re-executes module code, updating the module object in `sys.modules`. Useful for dev/REPL.

**Q: How does Python find modules?**
A: Searches `sys.path`: script dir → `PYTHONPATH` → stdlib → `site-packages`.

**Q: What's the `src/` layout?**
A: Package code in `src/mypackage/` — avoids accidental imports from working dir, matches installed structure.

---

## Key Takeaways

1. **Module** = `.py` file. **Package** = directory with `__init__.py` (or PEP 420 namespace package).
2. **`__init__.py`** runs on first import — use for exports (`__all__`), package init, lazy imports.
3. **Absolute imports** preferred — unambiguous, work everywhere. Relative imports only inside packages.
4. **`importlib`** — dynamic imports (`import_module`), reloading (`reload`), loading from path.
5. **`importlib.resources`** — read package data files (text/binary) without filesystem assumptions.
6. **`runpy`** — execute modules/files as `__main__` programmatically.
7. **`sys.path`** controls module search — prefer virtual envs + `pip install -e .` over manual manipulation.
8. **`pyproject.toml`** — modern packaging standard. Use `[project]`, `[build-system]`, optional deps.
9. **Circular imports** — fix with lazy imports (inside functions) or restructuring.
10. **`__name__ == "__main__"`** — guard for script-only code (tests, demos).

---

## Flashcards

See: [flashcards.md](../flashcards.md), [flashcards-fa.md](../flashcards-fa.md)

## Progress

- [ ] Read Python Cookbook Ch 7 — Modules & Packages
- [ ] Practice: creating packages, `__init__.py` patterns, relative imports
- [ ] Practice: importlib.import_module, reload, resources
- [ ] Practice: pyproject.toml, pip install -e, building distributions
- [ ] Practice: fixing circular imports, namespace packages
