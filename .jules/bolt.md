## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-11-20 - [Byte Templates in Proof of Work Loops]
**Learning:** Calling `.encode()` on strings in a tight loop like Proof of Work mining introduces unnecessary overhead. By using a pre-encoded byte string template (e.g., `b'{"nonce": %d' + escaped_suffix`) and simple byte formatting (`template % nonce`), we avoid encoding strings in every iteration. Hoisting the `hashlib.sha256` lookup also slightly boosts performance.
**Action:** When working with JSON-like strings in hot loops (like hashing), pre-compute a byte template, safely escape formatting characters (`%` -> `%%`), and use `%` byte formatting to eliminate `.encode()` and dictionary lookup overhead.
