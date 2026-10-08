## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2023-10-24 - Pre-compute Byte String Templates for Hashing
**Learning:** In heavily utilized loop constructs (like Proof of Work mining), string concatenation and UTF-8 encoding (`.encode()`) on every iteration are significant bottlenecks.
**Action:** Instead of dynamically building and encoding strings inside the loop, pre-compute static segments as a byte string template (e.g., `template = b'{"nonce": %d' + suffix_bytes`) and leverage Python's fast C-implemented `b"..." % (value,)` byte formatting. Always be sure to safely escape `%` characters in any injected payloads via `.replace(b'%', b'%%')` to prevent format string errors. Also, hoist dictionary attribute lookups (`hashlib.sha256`) outside the tight loop.
