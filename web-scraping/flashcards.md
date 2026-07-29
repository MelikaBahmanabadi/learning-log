# Web Scraping Flashcards — EN

Format: `Q | A | sub-topic | tier | New/Known/Needs Review | last tested`

---

## T0 · http-semantics

Q: What is the difference between GET and POST at the wire level?  
A: GET has no body; params go in the query string. POST carries a body (form-encoded, JSON, multipart). Server state change expected only on POST.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: What does a scraper actually receive — rendered page or raw response?  
A: Raw HTTP response body — bytes the server sends before any JavaScript executes. Rendered DOM only exists in a browser.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: What is the Host header and why is it mandatory in HTTP/1.1?  
A: Tells the server which virtual host to serve. Without it, a shared-IP server can't route the request — RFC 7230 requires it.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: Status code 429 — what should a scraper do?  
A: Read Retry-After header. Back off exactly that many seconds, then retry. Never retry immediately.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: What is the difference between 301 and 302 redirects?  
A: 301 = permanent (client may cache and skip original URL forever). 302 = temporary (re-check original next time). Both require following Location header.  
`sub-topic: redirects-cookies | tier: T0 | New | —`

Q: What does `Transfer-Encoding: chunked` mean for a scraper reading the body?  
A: Body arrives in size-prefixed chunks; don't buffer the raw body — let the HTTP client reassemble. Scraping the raw socket directly will break.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: Why should you never use `requests` with no timeout in production?  
A: A slow or hanging server holds your thread/coroutine forever, starving the pool. Always pass `timeout=(connect_s, read_s)`.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: What is content negotiation and how does it affect scraping?  
A: Server picks response format based on `Accept` header. Sending `Accept: application/json` may return JSON instead of HTML — cheaper to parse.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: What HTTP method signals idempotency and why does it matter for retries?  
A: GET, HEAD, PUT, DELETE are idempotent — safe to retry on network failure. POST is not — retrying a payment or form submit causes duplicate side-effects.  
`sub-topic: http-semantics | tier: T0 | New | —`

Q: What are the three parts of an HTTP response?  
A: Status line (version + code + reason), headers (key:value metadata), body (payload bytes).  
`sub-topic: http-semantics | tier: T0 | New | —`

---

## T0 · redirects-cookies

Q: What is a cookie jar and why must a scraper maintain one?  
A: Server-side session identity is stored in cookies. Without persisting them across requests, each request is treated as a new anonymous visitor — login state lost.  
`sub-topic: redirects-cookies | tier: T0 | New | —`

Q: What does the `Secure` flag on a cookie mean?  
A: Cookie sent only over HTTPS. A scraper using HTTP will never receive or send it — ensures you scrape the HTTPS endpoint.  
`sub-topic: redirects-cookies | tier: T0 | New | —`

Q: What does `SameSite=Strict` on a cookie do to a scraper?  
A: Cookie is sent only when request origin matches cookie domain. Cross-origin automated requests (e.g. API calls from different domain) won't include it.  
`sub-topic: redirects-cookies | tier: T0 | New | —`

---

## T0 · encodings

Q: How do you determine the encoding of an HTTP response reliably?  
A: Check `Content-Type` header first (`charset=utf-8`). Fall back to `<meta charset>` in HTML. Never assume UTF-8 silently — use `response.apparent_encoding` only as last resort.  
`sub-topic: encodings | tier: T0 | New | —`

Q: What breaks when you decode bytes as UTF-8 but the page is Windows-1252?  
A: UnicodeDecodeError on bytes 0x80–0x9F (€, curly quotes, etc.) — those bytes are undefined in UTF-8 but valid in cp1252.  
`sub-topic: encodings | tier: T0 | New | —`

---

## T0 · url-normalization

Q: Why must you normalize URLs before deduplicating a crawl frontier?  
A: `http://example.com/page`, `http://example.com/page?`, `HTTP://EXAMPLE.COM/page` all resolve to the same resource. Without normalization, you crawl the same page multiple times.  
`sub-topic: url-normalization | tier: T0 | New | —`

Q: What is percent-encoding and when does a scraper need to decode it?  
A: URL-safe encoding: space → `%20`, non-ASCII → `%XX`. Decode before display or storage; re-encode before sending. `urllib.parse.unquote` / `quote`.  
`sub-topic: url-normalization | tier: T0 | New | —`

---

## T0 · robots-sitemaps

Q: What does `Crawl-delay` in robots.txt legally/practically mean?  
A: Polite minimum seconds between requests to that domain. Not enforced by servers — but ignoring it increases ban risk and may create legal exposure.  
`sub-topic: robots-sitemaps | tier: T0 | New | —`

Q: What is a sitemap.xml and why is it valuable before crawling?  
A: XML index of all canonical URLs a site wants indexed. Using it means you skip discovery crawling entirely — faster, complete, avoids honeypot traps.  
`sub-topic: robots-sitemaps | tier: T0 | New | —`

---

## T1 · httpx-client

Q: Why prefer `httpx.AsyncClient` over `requests.Session` for I/O-bound scraping?  
A: `requests` is synchronous — one blocked read blocks the thread. `httpx.AsyncClient` with `asyncio` runs hundreds of concurrent fetches in one thread with no GIL contention.  
`sub-topic: httpx-client | tier: T1 | New | —`

Q: What is connection pooling and why does it matter at scale?  
A: Reusing open TCP+TLS connections across requests avoids 3-way handshake + TLS handshake overhead per request (~100–300ms each). `httpx.AsyncClient` pools by default when kept open as a context manager.  
`sub-topic: httpx-client | tier: T1 | New | —`

Q: What is the correct timeout tuple signature in httpx?  
A: `httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0)` — never use a single float for production; read and connect have different failure modes.  
`sub-topic: httpx-client | tier: T1 | New | —`

---

## T1 · selectors

Q: When should you prefer CSS selectors over XPath?  
A: CSS for class/id/attribute targeting on HTML — shorter syntax, browser-native. XPath when you need text() matching, parent axis traversal, or node position predicates.  
`sub-topic: selectors | tier: T1 | New | —`

Q: Why are `nth-child` and generated class name selectors fragile?  
A: They depend on DOM position or obfuscated class names that change on every deploy. Use semantic attributes (`data-testid`, `itemprop`, `aria-label`) or structured data instead.  
`sub-topic: selectors | tier: T1 | New | —`

Q: What does `soup.select_one("div.product > span.price")` do differently from `soup.select("div.product span.price")`?  
A: `>` is a direct child combinator — span must be immediate child of div. Space is descendant — span can be nested anywhere inside div.  
`sub-topic: selectors | tier: T1 | New | —`

---

## T1 · extraction-contracts

Q: What is an extraction contract and why does it matter?  
A: A typed schema (e.g. Pydantic model) that validates extracted fields. Without it, empty/null fields silently pass through and corrupt downstream storage.  
`sub-topic: extraction-contracts | tier: T1 | New | —`

Q: What is the "empty result treated as success" failure mode?  
A: Scraper returns `[]` when the selector finds nothing — maybe the page structure changed. Without a min-result guard, the pipeline writes zero rows and nobody notices for days.  
`sub-topic: extraction-contracts | tier: T1 | New | —`

---

## T1 · structured-data

Q: What is JSON-LD and why should you check for it before writing a selector?  
A: `<script type="application/ld+json">` embeds structured machine-readable data (Schema.org). Parsing it is O(1) and immune to HTML layout changes — always check Network tab first.  
`sub-topic: structured-data | tier: T1 | New | —`

Q: What are Open Graph meta tags and what data do they reliably carry?  
A: `<meta property="og:title">`, `og:image`, `og:description` — set by publishers for social sharing previews. Stable, parseable without complex selectors.  
`sub-topic: structured-data | tier: T1 | New | —`
