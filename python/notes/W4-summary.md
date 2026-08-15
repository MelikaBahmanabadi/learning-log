# Ch 4: Strings, Bytes & Text Processing

## Books Covered
- **Fluent Python (2nd Ed)** — Ch 4: Text versus Bytes (Unicode code points, encodings, UTF-8, bytes vs str)
- **Python Cookbook (3rd Ed)** — Ch 2: Strings and Text (splitting, matching, search & replace, regex, unicode, whitespace, string formatting)
- **Effective Python (3rd Ed)** — Item 3: Know the differences between bytes, str, and unicode

## Roadmap Sections Covered
- ✅ String basics, methods, manipulation
- ✅ f-strings & format specifiers (revisited)
- ✅ Unicode: code points, encodings, UTF-8 vs UTF-16 vs UTF-32
- ✅ bytes, bytearray, decoding & encoding errors
- ✅ Text vs binary file modes
- ✅ Regex: pattern matching, groups, substitution
- ✅ String alignment, padding, splitting & joining
- ✅ Normalization, casefold, sanitizing

---

## 4.1 str vs bytes vs bytearray

> **Sources**: [Unicode Standard, Section 3.9](https://unicode.org/versions/latest/ch03.pdf) for encoding forms; [docs.python.org/3/library/stdtypes.html#text-sequence-type-str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)

Python has three text-ish types:

```python
# str — immutable Unicode text (code points)
s = "Hello"          # str
type(s)              # <class 'str'>

# bytes — immutable binary (integers 0–255)
b = b"Hello"         # bytes (ASCII literal shortcut)
type(b)              # <class 'bytes'>
b[0]                 # 72 — int, not str!

# bytearray — mutable binary
ba = bytearray(b"Hello")
ba[0] = 104          # mutate in place
bytes(ba)            # b"hello"
```

**Key insight:** `str` is a sequence of **code points** (Unicode characters). `bytes`/`bytearray` are sequences of **bytes** (integers 0–255).

| Type | Content | Mutable | Literal |
|------|---------|---------|---------|
| `str` | Unicode code points | No | `"Hello"` / `'Hello'` |
| `bytes` | Bytes (0–255) | No | `b"Hello"` |
| `bytearray` | Bytes (0–255) | Yes | `bytearray(b"Hello")` |

```python
# bytes indexing gives ints
b"ABC"[0]            # 65

# str indexing gives single-char str
"ABC"[0]             # "A"
```

### Conversion Between str and bytes

```python
s = "héllo"                     # str, 5 code points
b = s.encode("utf-8")           # b'h\xc3\xa9llo' — code points → bytes
s2 = b.decode("utf-8")          # "héllo" — bytes → code points

# The é takes 2 bytes in UTF-8 — len differs
len(s)                          # 5 (code points)
len(b)                          # 6 (bytes)
```

**Effective Python Item 3 rule:**
- Bytes → str: `b.decode(encoding)` — decode at the **boundary** (network, files)
- str → bytes: `s.encode(encoding)` — encode at the **edge**
- Never mix `bytes` and `str` with `+` or `==` — raises `TypeError`

---

## 4.2 Encoding Errors

```python
s = "héllo"
s.encode("ascii")               # UnicodeEncodeError! é not in ASCII
s.encode("ascii", errors="ignore")    # b'hllo' — silently drop
s.encode("ascii", errors="replace")   # b'h?llo' — substitute ?
s.encode("ascii", errors="backslashreplace")  # b'h\\xe9llo' — escape

# Decoding side
b = b"\xff\xfe"
b.decode("utf-8")                     # UnicodeDecodeError
b.decode("utf-8", errors="replace")   # 'U+FFFD' — replacement char (U+FFFD)
b.decode("utf-8", errors="ignore")    # '' — drop invalid
```

**Best practice:** use `errors="replace"` or `"backslashreplace"` for logging/tolerant code. Raise loudly during development so you catch problems early.

### The 'surrogateescape' Handler

```python
# Round-trip unknown bytes when filesystem/latin-1 boundary needs it
data = b"\xff\xfe"
s = data.decode("utf-8", errors="surrogateescape")  # '\udcff\udcfe'
s.encode("utf-8", errors="surrogateescape")          # b'\xff\xfe' — exact round-trip
```

Used internally by `os.listdir()` on Unix — lets you carry bytes you can't decode.

---

## 4.3 Unicode Code Points & Encodings

```python
# Code point: the integer that identifies a character
ord("A")             # 65
ord("é")             # 233
chr(65)              # "A"

# A code point's byte representation depends on encoding
s = "A"
s.encode("utf-8")    # b"A" — 1 byte
s.encode("utf-16")   # b'\xff\xfeA\x00' — 2 bytes + BOM

"é".encode("utf-8")     # b'\xc3\xa9' — 2 bytes
"é".encode("utf-16")    # b'\xe9\x00' — 2 bytes
"😀".encode("utf-8")    # b'\xf0\x9f\x98\x80' — 4 bytes (emoji)
```

### Encoding Comparison

| Encoding | Min bytes | Max bytes | Notes |
|----------|-----------|-----------|-------|
| ASCII | 1 | 1 | 7-bit, 128 chars, no accents |
| UTF-8 | 1 | 4 | ASCII-compatible, default for web/Python source |
| UTF-16 | 2 | 4 | Windows/Linux legacy, BOM |
| UTF-32 | 4 | 4 | Fixed-width, wasteful |
| latin-1 / iso8859-1 | 1 | 1 | 256 chars, maps bytes 0–255 to U+0000–U+00FF |

**UTF-8 rules:**
- ASCII characters stay 1 byte (backward compatible with ASCII)
- Code points U+0080–U+07FF → 2 bytes, U+0800–U+FFFF → 3 bytes, beyond → 4 bytes
- Default for Python source, JSON, and ~98% of the web

### BOM — Byte Order Mark

```python
# UTF-16 BOM indicates byte order
data = "A".encode("utf-16")     # b'\xff\xfeA\x00' — FF FE = little-endian
data.decode("utf-16")           # "A" (BOM consumed, order detected)

# UTF-8 BOM (optional, sometimes in files)
b"\xef\xbb\xbf".decode("utf-8")  # '﻿'
```

---

## 4.4 Normalization & Casefold

> **Sources**: [Unicode Standard Annex #15](https://unicode.org/reports/tr15/) for normalization; [Unicode Standard, Section 3.13](https://unicode.org/versions/latest/ch03.pdf) for case folding

```python
# Unicode normalization: canonically equivalent sequences
from unicodedata import normalize, combining, name

n1 = "café"        # "café" — precomposed é (U+00E9)
n2 = "café"       # "café" — e + combining accent (U+0301)

n1 == n2                          # False — different code points
normalize("NFC", n2) == n1        # True — NFC composes
normalize("NFD", n1)              # decomposes: "café"
len(normalize("NFD", "café"))     # 5 (c,a,f,e,´)

# Forms
# NFC  — composed (canonical) — default for most text
# NFD  — decomposed
# NFKC / NFKD — compatibility (folds ligatures like ½ → 1/2) — use with care

# Case-insensitive comparison
"Straße".lower() == "strasse".lower()     # False
"Straße".casefold() == "strasse".casefold()  # True — casefold handles ß

# Remove combining marks (accent stripping)
def strip_accents(s):
    return "".join(c for c in normalize("NFD", s) if not combining(c))

strip_accents("café")         # "cafe"
```

**Rule:** use `casefold()` for case-insensitive comparison, `NFC` normalization before comparison, and `NFD` + `combining()` filter for accent stripping.

---

## 4.5 String Formatting (revisited)

```python
# f-strings (3.6+) — preferred
name, qty, price = "Melika", 3, 19.99
f"{name} bought {qty} {qty*price:.2f}"   # "Melika bought 3 59.97"

# Format spec mini-language
f"{price:.2f}"        # 19.99
f"{price:,.2f}"       # 19.99 → 1,234.56 with thousands sep
f"{qty:05d}"          # 00003 — zero-pad width 5
f"{price:<10}"        # left align width 10
f"{price:>10}"        # right align
f"{price:^10}"        # center
f"{0.5:.0%}"          # 50% — percent
f"{price:+}"          # +19.99 — explicit sign
f"{1234_5678:x}"      # hex (underscores = digit separators)

# Alignment via str methods
"hello".ljust(10)     # 'hello     '
"hello".rjust(10)     # '     hello'
"hello".center(10)    # '  hello   '
"hello".zfill(10)     # '00000hello'

# str.format (older, still in libraries)
"{}, {}!".format("Hello", "World")
"{0} then {1} then {0}".format("a", "b")   # positional reuse
"{name} is {age}".format(name="Melika", age=25)  # keyword

# %-formatting (legacy)
"%s — %d" % ("hello", 42)
```

**Modern guidance:** f-strings for your own code. `str.format` only when the template comes from user data (no f-string equivalent).

### Template strings (PEP 292) — safe for user input

```python
from string import Template
t = Template("Hello $name, you have $n items")
t.substitute(name="Melika", n=3)    # "Hello Melika, you have 3 items"
t.safe_substitute(name="Melika")    # missing $n left as-is, no KeyError
```

---

## 4.6 Splitting, Joining & Stripping

```python
s = " one  two   three "

# split — whitespace (any run) or explicit sep
s.split()              # ["one", "two", "three"] — collapses all whitespace
"a,b,c".split(",")     # ["a", "b", "c"]
"a,b,c".rsplit(",", 1) # ["a,b", "c"] — split from the right
"a\nb\nc".splitlines() # ["a", "b", "c"] — handles all line breaks
s.split(maxsplit=1)    # ["one", "two   three "] — limit splits

# join — the separator is the string being called
" ".join(["a", "b", "c"])      # "a b c"
"-".join("abc")                # "a-b-c"
", ".join(str(x) for x in [1, 2, 3])  # "1, 2, 3"

# strip / lstrip / rstrip — removes any char in the set
"  hi  ".strip()               # "hi"
"xxhiyy".strip("xy")           # "hi" — removes chars, not substring
"http://x".strip("h")          # "ttp://x" — DANGER: strips h/t/p anywhere
"#tag#".strip("#")             # "tag"
```

**Gotcha:** `str.strip(chars)` removes *any character in the set*, not a literal string — `"http://".strip("/")` strips all `/` at both ends, not just one.

```python
# Removesuffix / removeprefix (Python 3.9+) — literal-safe
"README.md".removesuffix(".md")   # "README"
"file.txt".removeprefix("file")   # ".txt"
```

---

## 4.7 Regex — `re` Module

### Quick Reference

| Pattern | Meaning |
|---------|---------|
| `.` | Any char except newline |
| `^` / `$` | Start / end of string |
| `\d` | Digit (`[0-9]`) |
| `\w` | Word char (`[a-zA-Z0-9_]`) |
| `\s` | Whitespace |
| `\b` | Word boundary |
| `*` / `+` / `?` | 0+, 1+, 0 or 1 |
| `{m,n}` | m to n repeats |
| `[abc]` | Char class |
| `(a\|b)` | Alternation |
| `(...)` | Capturing group |
| `(?:...)` | Non-capturing group |
| `(?P<name>...)` | Named group |

### Core Functions

```python
import re

text = "Orders: #42 and #100, total 142 items"

# re.match — only at start
re.match(r"\d+", "42 apples")      # match (42)
re.match(r"\d+", "apples 42")      # None — not at start

# re.search — anywhere
re.search(r"\d+", text)            # match at "142"

# re.findall — all matches as list
re.findall(r"#(\d+)", text)        # ["42", "100"] — group contents

# re.finditer — iterate match objects (lazy)
for m in re.finditer(r"\d+", text):
    m.group(), m.start(), m.end()   # ("142", 26, 29)

# re.split
re.split(r"[,\s]+", "a, b  c")     # ["a", "b", "c"]

# re.sub — replace
re.sub(r"\d+", "N", "a1 b22")      # "aN bN"
re.sub(r"(\w+) (\w+)", r"\2 \1", "hello world")  # "world hello"

# re.escape — treat a literal string as a pattern
re.escape("a.b*c")                 # 'a\\.b\\*c'
```

### Compiling Patterns

```python
# Pre-compile for reuse (module-level cache anyway, but clearer)
phone = re.compile(r"(\d{3})-(\d{3})-(\d{4})")
m = phone.search("Call 123-456-7890")
m.group(0)          # "123-456-7890" — whole match
m.group(1)          # "123" — first group
m.groups()          # ("123", "456", "7890") — all groups
m.groupdict()       # {} — unless named

# Named groups
named = re.compile(r"(?P<area>\d{3})-(?P<num>\d{4})")
m = named.search("123-4567")
m.group("area")     # "123"
m.groupdict()       # {"area": "123", "num": "4567"}
```

### Flags

```python
re.search(r"world", "HELLO WORLD", re.IGNORECASE)   # match
re.search(r"^a", "b\na", re.MULTILINE)              # match — ^ matches per line
re.search(r".+", "a\nb", re.DOTALL)                 # match — . matches \n
re.findall(r"\w+", "é clé", re.UNICODE)             # unicode-aware (default for str)
```

### Common Recipe: Word Count

```python
from collections import Counter
words = re.findall(r"\w+", text.lower())
counts = Counter(words)
```

---

## 4.8 Text Files & Encoding in Practice

```python
# Text mode — str, handles encoding + newline translation
with open("data.txt", encoding="utf-8") as fh:
    text = fh.read()            # str

# Explicit encoding — NEVER rely on locale default
with open("data.txt", "w", encoding="utf-8") as fh:
    fh.write("café")            # encoded as UTF-8

# Binary mode — bytes, no translation
with open("data.bin", "rb") as fh:
    raw = fh.read()             # bytes

# Newline handling (universal newlines)
# text mode converts \r\n / \r → \n on read; default newline on write

# UTF-8 with error tolerance when reading external files
with open("data.txt", encoding="utf-8", errors="replace") as fh:
    text = fh.read()
```

**PEP 8 / best practices:**
- Always pass `encoding=` when opening text files
- Use UTF-8 as the default everywhere (source files, JSON, files)
- Decode bytes at the I/O boundary — never inside business logic

---

## 4.9 Sanitizing & Cleaning Text

```python
import unicodedata

def clean_text(s):
    s = unicodedata.normalize("NFKD", s)      # compatibility decompose
    s = s.encode("ascii", errors="ignore").decode("ascii")  # strip non-ASCII
    s = " ".join(s.split())                    # collapse whitespace
    return s

clean_text("cafe — test")      # "cafe  test" (— dropped, extra spaces collapsed)

# Keep only allowed chars
import re
re.sub(r"[^a-zA-Z0-9 ]", "", "Hello, World! 42")   # "Hello World 42"

# Remove HTML-ish tags (naive — use a parser for real HTML)
re.sub(r"<[^>]+>", "", "<p>Hello <b>World</b></p>")  # "Hello World"
```

**Caution:** For real HTML/XML parsing, use a parser (`html.parser`, `lxml`, `BeautifulSoup`) — regex is fragile.

---

## 4.10 Practice Checklist

- [ ] Encode/decode str ↔ bytes with explicit encodings
- [ ] Handle encoding errors with `errors="replace"` / `"surrogateescape"`
- [ ] Normalize text with NFC/NFD, compare with `casefold()`
- [ ] Format strings with f-strings + format spec mini-language
- [ ] Split/join/strip with whitespace handling
- [ ] Use regex: `match`, `search`, `findall`, `finditer`, `sub`, groups, flags
- [ ] Open text files with explicit `encoding="utf-8"`
- [ ] Clean text: strip accents, collapse whitespace, keep allowed chars

---

## Flashcards

See: [flashcards.md](../flashcards.md), [flashcards-fa.md](../flashcards-fa.md)

## Progress

- [ ] Read Fluent Python Ch 4 — Text versus Bytes
- [ ] Read Python Cookbook Ch 2 — Strings and Text
- [ ] Practice: encode/decode, normalization, regex, formatting
- [ ] Sanitize a real text dataset (accents, HTML, whitespace)
