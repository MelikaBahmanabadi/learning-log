# T0 · http-semantics

## 1 — Mental Model

When your scraper calls `GET https://example.com/products`, it is not opening a file.
It is executing a protocol exchange:

```
Client (scraper)
  │
  ├─ DNS resolution: example.com → 93.184.216.34
  ├─ TCP 3-way handshake (SYN / SYN-ACK / ACK)       ~1 RTT
  ├─ TLS 1.3 handshake (ClientHello / ServerHello)   ~1 RTT
  │
  ├─ HTTP REQUEST (bytes on the wire)
  │     GET /products HTTP/1.1
  │     Host: example.com
  │     User-Agent: mybot/1.0
  │     Accept: text/html,application/json;q=0.9
  │     Accept-Encoding: gzip, br
  │     Connection: keep-alive
  │
  └─ HTTP RESPONSE
        HTTP/1.1 200 OK
        Content-Type: text/html; charset=utf-8
        Content-Encoding: gzip
        Transfer-Encoding: chunked
        Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Lax
        
        <compressed body bytes>
```

Key insight: **the scraper receives raw bytes before any JavaScript executes.**  
What you see in a browser ≠ what the server sends. DevTools → Network → Disable cache → look at the raw Response tab, not the rendered Elements tab.

---

## 2 — Reference Implementation

Production-grade single-page fetch with typed signature, explicit timeouts, bounded retries, structured logging, no global state:

```python
"""http_fetch.py — production HTTP fetch with typed API."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Final

import httpx

logger = logging.getLogger(__name__)

# ── configuration ────────────────────────────────────────────────────────────

DEFAULT_TIMEOUT: Final = httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0)
MAX_RETRIES: Final[int] = 3
BACKOFF_BASE: Final[float] = 2.0  # seconds
RETRYABLE_CODES: Final[frozenset[int]] = frozenset({429, 500, 502, 503, 504})


@dataclass
class FetchResult:
    url: str
    status: int
    body: bytes
    headers: dict[str, str] = field(default_factory=dict)


# ── core fetch ───────────────────────────────────────────────────────────────

def fetch(
    url: str,
    *,
    client: httpx.Client,
    headers: dict[str, str] | None = None,
    max_retries: int = MAX_RETRIES,
) -> FetchResult:
    """Fetch *url* with bounded retries and explicit Retry-After handling.

    Design choices:
    1. Caller-injected client — no hidden global Session; allows connection
       pooling and clean test injection.
    2. Explicit timeout tuple — connect and read have different failure modes;
       a single scalar masks which one fired.
    3. Retry-After honoured exactly — servers set it for a reason; ignoring it
       leads to IP bans, not faster scraping.
    """
    extra_headers: dict[str, str] = {
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, br",
        **(headers or {}),
    }

    last_exc: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.get(url, headers=extra_headers)
            logger.info("%s %s → %d (attempt %d)", "GET", url, resp.status_code, attempt)

            if resp.status_code in RETRYABLE_CODES:
                wait = float(resp.headers.get("Retry-After", BACKOFF_BASE ** attempt))
                logger.warning("retryable %d; sleeping %.1fs", resp.status_code, wait)
                time.sleep(wait)
                continue

            resp.raise_for_status()
            return FetchResult(
                url=url,
                status=resp.status_code,
                body=resp.content,
                headers=dict(resp.headers),
            )

        except httpx.TimeoutException as exc:
            last_exc = exc
            wait = BACKOFF_BASE ** attempt
            logger.warning("timeout on attempt %d; retrying in %.1fs", attempt, wait)
            time.sleep(wait)

        except httpx.HTTPStatusError as exc:
            # non-retryable 4xx — do not retry
            logger.error("non-retryable HTTP %d: %s", exc.response.status_code, url)
            raise

    raise RuntimeError(
        f"fetch failed after {max_retries} attempts: {url}"
    ) from last_exc


# ── usage ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    with httpx.Client(timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        result = fetch("https://quotes.toscrape.com", client=client)
    print(f"status={result.status} body_len={len(result.body)}")
```

**Three design choices and the alternative rejected:**

| Choice | Alternative rejected | Reason |
|--------|---------------------|--------|
| Caller-injected `httpx.Client` | Global `requests.Session` | Global state breaks concurrent tests; pool is not shared across coroutines |
| `httpx.Timeout(connect=5, read=30)` | Single `timeout=30` | Connect timeout and read timeout have different causes; a single value masks which fired |
| Sleep exactly `Retry-After` seconds | Exponential backoff only | Server sets `Retry-After` for capacity reasons; ignoring it burns your IP allowance |

---

## 3 — Failure Atlas

| Symptom | Real Cause | Fix | Production Detection |
|---------|-----------|-----|---------------------|
| `ReadTimeout` after exactly 30s | Server stalled after partial send (chunked encoding, DB lock) | Set `read=30` + log partial bytes received | Alert on timeout rate > 1% per domain |
| Empty `response.text` despite `200 OK` | `Content-Encoding: br` (Brotli) and `requests` doesn't decode it | Use `httpx` (decodes br) or add `brotli` package | Log `content-length` vs `len(body)` |
| Intermittent `ConnectionResetError` | Server closes keep-alive after N requests | Set `limits=httpx.Limits(max_keepalive_requests=50)` | Track connection reuse rate |
| Correct response on first run, 403 after 1000 requests | Rate limit triggered on cookie-less requests after rotation | Persist cookies across rotations; re-login when session expires | Track 403 rate per session |
| **Scale-only**: scraper slows after 6 hours | Connection pool exhausted — leaked clients not closed | Always use `with httpx.Client()` or explicit `client.close()` | Monitor open file descriptors |
| **Week-only**: 200 but wrong data | Page A/B test variant based on user agent or geo — scraper gets different version | Pin `User-Agent`, fix geo via proxy, add content fingerprint check | Hash first 500 bytes of body; alert on deviation |

---

## 4 — Cost & Layer Choice

| Layer | Req/s (1 worker) | RAM/worker | Cost/1M pages | When to use |
|-------|-----------------|------------|---------------|-------------|
| Raw `httpx` async | ~200–500 | ~50 MB | ~$0.10 (EC2 t3.small) | Static HTML, JSON APIs |
| `httpx` sync | ~20–50 | ~40 MB | ~$0.50 | Simple scripts, low volume |
| Selenium (headless Chrome) | ~3–8 | ~300 MB | ~$5–15 | Only when JS renders critical data not in any API |
| Playwright async | ~8–20 | ~200 MB | ~$3–8 | JS-heavy SPAs when no API found |

**Rule:** Always attempt static HTTP first. Browser cost is 10–50× raw HTTP.  
If a page needs JS: check Network tab for XHR/fetch calls first — often a private JSON API is available.

---

## 5 — HTTP Status Codes Reference

| Code | Meaning | Scraper Action |
|------|---------|---------------|
| 200 | OK | Parse body |
| 201 | Created | (POST response) |
| 301 | Permanent Redirect | Follow; update stored URL |
| 302 | Temporary Redirect | Follow; keep original URL |
| 400 | Bad Request | Fix request format; don't retry |
| 401 | Unauthorized | Fix auth headers; don't retry blindly |
| 403 | Forbidden | Likely IP/fingerprint ban — rotate |
| 404 | Not Found | Remove from frontier |
| 429 | Too Many Requests | Read `Retry-After`; back off |
| 500 | Internal Server Error | Retry with backoff (server-side transient) |
| 503 | Service Unavailable | Retry with backoff + `Retry-After` |

---

## Open Questions

- How does HTTP/2 multiplexing change the connection model for scrapers?
- When does `h2c` (HTTP/2 cleartext) appear and how does httpx handle it?
- What TLS fingerprint does httpx present and how does it compare to a real Chrome?
