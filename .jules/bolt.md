## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-05-23 - [Proof of Work Loop Optimization]
**Learning:** String concatenation and `.encode()` inside a tight Proof of Work mining loop (`while` loop) introduces unnecessary object creation and overhead. Replacing string manipulation with byte string templates (`b'{"nonce": %d' + suffix_bytes`) and string interpolation (`template % nonce`), combined with hoisting `hashlib.sha256`, can yield significant speedups.
**Action:** Always use byte string templates and pre-compute as much as possible before entering a hashing loop. Remember to safely escape `%` as `%%` when converting the static JSON suffix to bytes to prevent format string vulnerabilities.
