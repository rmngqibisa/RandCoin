## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-11-20 - [Proof of Work Loop Optimization]
**Learning:** In highly intensive CPU loops like Proof of Work mining, string concatenation (`str + str`) combined with `.encode()` in every iteration adds significant overhead. Replacing this with pre-computed byte format templates (e.g., `b'{"nonce": %d' + suffix_bytes`) and using `%` formatting (`template % nonce`), along with hoisting local variable lookups (`sha256 = hashlib.sha256`), avoids `.encode()` overhead and reduces execution time. (Always safely escape `%` as `%%` in the payload).
**Action:** Use pre-computed byte formatting and hoist function lookups in critical inner loops where string manipulation and encoding are bottleneck operations.
