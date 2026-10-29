## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-10-29 - [Byte Templating in PoW Mining]
**Learning:** Using Python byte-formatting (`b'...' % value`) instead of string concatenation and `.encode()` in a tight Proof of Work mining loop significantly reduces allocation and UTF-8 encoding overhead. Also, `%` characters in JSON payloads must be manually escaped (using `%%`) before creating the format string template to avoid `TypeError` formatting bugs.
**Action:** When optimizing loop-heavy cryptographic hashing of stringified data, pre-compute static parts into byte string templates with proper escaping, and hoist function lookups (`hashlib.sha256`) outside the loop.
