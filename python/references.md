# Python Learning Log — References & Citations

This file documents verifiable sources for version-sensitive, implementation-specific, and complexity claims in the flashcards and notes.

## Dict Internals & Implementation

### Hash Table Implementation (CPython)
- **Claim**: Dict uses open addressing with probing for collision resolution
- **Source**: [CPython `Objects/dictobject.c`](https://github.com/python/cpython/blob/main/Objects/dictobject.c) — `lookdict()` function
- **Also**: Raymond Hettinger, ["Python's dictionary implementation"](https://mail.python.org/pipermail/python-dev/2012-December/123028.html) (python-dev, 2012)

### Load Factor & Resizing
- **Claim**: Table resizes when load factor exceeds ~2/3
- **Source**: CPython `dictobject.c` — `USABLE_FRACTION` macro defines threshold as 2/3
- **Code**: `#define USABLE_FRACTION(n) (((n) << 1) / 3)` in CPython 3.12+

### Compact Dict (Python 3.6+)
- **Claim**: Python 3.6+ uses compact array representation, reducing memory
- **Source**: [PEP 412](https://peps.python.org/pep-0412/) — "Key-sharing dictionary"
- **Also**: [PEP 468](https://peps.python.org/pep-0468/) — "Preserving the order of **kwargs in a function"

### Insertion Order Guarantee
- **Claim**: Dicts preserve insertion order (language guarantee, Python 3.7+)
- **Source**: [PEP 468](https://peps.python.org/pep-0468/) — specifies insertion-order preservation as language guarantee
- **Note**: CPython 3.6 implemented this; Python 3.7 made it a language guarantee

## Complexity Guarantees

### Dict Operations
- **Claim**: `key in dict` — O(1) average
- **Source**: [Python Wiki: Time Complexity](https://wiki.python.org/moin/TimeComplexity) — dict membership O(1) average, O(n) worst case
- **Also**: [Python Docs: Data Structures](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

### List Operations
- **Claim**: `list.append()` — O(1) amortized
- **Source**: [Python Wiki: Time Complexity](https://wiki.python.org/moin/TimeComplexity) — list append O(1) amortized
- **Note**: List over-allocates; most appends don't trigger resize

### Set Operations
- **Claim**: Set membership O(1) average
- **Source**: [Python Wiki: Time Complexity](https://wiki.python.org/moin/TimeComplexity) — set `x in s` O(1) average

## Unicode & Encoding

### Normalization
- **Claim**: `unicodedata.normalize("NFC", s)` composes canonically
- **Source**: [Unicode Standard Annex #15](https://unicode.org/reports/tr15/) — Unicode Normalization Forms
- **Python**: [Docs: unicodedata.normalize](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize)

### Casefold
- **Claim**: `casefold()` handles German ß → ss
- **Source**: [Unicode Standard, Section 3.13](https://unicode.org/versions/latest/ch03.pdf) — Default Case Folding
- **Python**: [Docs: str.casefold](https://docs.python.org/3/library/stdtypes.html#str.casefold)

### UTF-8/UTF-16/UTF-32
- **Claim**: UTF-8 is 1–4 bytes, ASCII-compatible; UTF-16 is 2–4 bytes
- **Source**: [Unicode Standard, Section 3.9](https://unicode.org/versions/latest/ch03.pdf) — Unicode Encoding Forms

## Standard Library Behavior

### defaultdict
- **Claim**: Factory called on missing key access via `d[key]`
- **Source**: [Docs: collections.defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)

### OrderedDict
- **Claim**: `move_to_end()` and order-sensitive equality
- **Source**: [Docs: collections.OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)

### Counter
- **Claim**: Arithmetic operations supported
- **Source**: [Docs: collections.Counter](https://docs.python.org/3/library/collections.html#collections.Counter)

### ChainMap
- **Claim**: Groups multiple dicts, mutations affect first dict only
- **Source**: [Docs: collections.ChainMap](https://docs.python.org/3/library/collections.html#collections.ChainMap)

### MappingProxyType
- **Claim**: Read-only dict wrapper
- **Source**: [Docs: types.MappingProxyType](https://docs.python.org/3/library/types.html#types.MappingProxyType)

### UserDict
- **Claim**: `UserDict` wraps `self.data` dict — safer than dict subclass
- **Source**: [Docs: collections.UserDict](https://docs.python.org/3/library/collections.html#collections.UserDict)

## Version-Specific Features

### Python 3.7
- **Feature**: Dict insertion order is language guarantee
- **Source**: [PEP 468](https://peps.python.org/pep-0468/)

### Python 3.8
- **Feature**: Positional-only parameters (`/`)
- **Source**: [PEP 570](https://peps.python.org/pep-0570/)

### Python 3.9
- **Feature**: Dict merge operators (`|`, `|=`, `|=`)
- **Source**: [PEP 584](https://peps.python.org/pep-0584/)
- **Feature**: `str.removeprefix()`, `str.removesuffix()`
- **Source**: [PEP 616](https://peps.python.org/pep-0616/)

### Python 3.10
- **Feature**: Structural pattern matching (`match/case`)
- **Source**: [PEP 634](https://peps.python.org/pep-0634/)

## Modules, Packages & Import System

### Module vs Package
- **Claim**: Module = single `.py` file; package = directory with `__init__.py` (or namespace package)
- **Source**: [Python Tutorial: Modules](https://docs.python.org/3/tutorial/modules.html)

### Regular Packages & `__init__.py`
- **Claim**: `__init__.py` runs on first import of the package or any submodule
- **Source**: [Python Reference: The import system — Regular packages](https://docs.python.org/3/reference/import.html#regular-packages)

### `__all__`
- **Claim**: Controls `from package import *`
- **Source**: [Python Tutorial: Importing * From a Package](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package)

### Absolute vs Relative Imports
- **Claim**: Absolute imports preferred (PEP 8); relative imports use `.` / `..`
- **Source**: [PEP 8 — Imports](https://peps.python.org/pep-0008/#imports), [PEP 328](https://peps.python.org/pep-0328/)

### Namespace Packages
- **Claim**: Packages without `__init__.py` merge multiple directories
- **Source**: [PEP 420](https://peps.python.org/pep-0420/)

### `importlib`
- **Claim**: `import_module()`, `reload()`, `util.spec_from_file_location()`
- **Source**: [Docs: importlib](https://docs.python.org/3/library/importlib.html), [PEP 451 — ModuleSpec](https://peps.python.org/pep-0451/)

### `importlib.resources.files()`
- **Claim**: `files()` / `read_text()` / `read_bytes()` API is Python 3.9+
- **Source**: [Docs: importlib.resources](https://docs.python.org/3/library/importlib.resources.html)

### `pkgutil`
- **Claim**: `get_data()`, `iter_modules()`
- **Source**: [Docs: pkgutil](https://docs.python.org/3/library/pkgutil.html)

### `runpy`
- **Claim**: `run_module()` / `run_path()` run code as `__main__`
- **Source**: [Docs: runpy](https://docs.python.org/3/library/runpy.html)

### `sys.path`
- **Claim**: Module search order — script dir → PYTHONPATH → stdlib → site-packages
- **Source**: [Docs: sys.path](https://docs.python.org/3/library/sys.html#sys.path)

### `__name__ == "__main__"`
- **Claim**: Guard for direct execution
- **Source**: [Docs: `__main__`](https://docs.python.org/3/library/__main__.html)

### Circular Imports
- **Claim**: Fix by lazy imports, restructuring, or importlib
- **Source**: [Python FAQ: Programming](https://docs.python.org/3/faq/programming.html)

### `src/` Layout & Packaging
- **Claim**: `src/mypackage/` layout avoids accidental imports from working dir
- **Source**: [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

### `pyproject.toml`
- **Claim**: Modern packaging config (PEP 517/518/621)
- **Source**: [PEP 621](https://peps.python.org/pep-0621/), [PEP 517](https://peps.python.org/pep-0517/)

### Editable Installs
- **Claim**: `pip install -e .` installs via symlinks
- **Source**: [PEP 660](https://peps.python.org/pep-0660/)

### Leading Underscore & Conditional Imports
- **Claim**: `_name` convention; `try/except ImportError` for optional deps
- **Source**: [PEP 8](https://peps.python.org/pep-0008/)

## References for Flashcard Citations

When a flashcard makes a version-sensitive or implementation-specific claim, cite:
- **PEP**: `PEP XXX` with link
- **Docs**: Python docs page
- **CPython**: Source file and function
- **Unicode**: Unicode Standard section

Example citation format in flashcards:
```
Q: How does Python's dict handle hash collisions?
A: Open addressing — probes next slots until finding empty slot. When load factor exceeds ~2/3, the table resizes. [CPython: Objects/dictobject.c, lookdict()]
```
