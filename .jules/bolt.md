## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-10-25 - [Byte String Templating in Proof of Work]
**Learning:** During Proof of Work mining loops, constructing strings and calling `.encode()` repeatedly adds significant overhead. Pre-encoding static parts and using byte string interpolation (e.g., `b'{"nonce": %d' + suffix_bytes` and `template % nonce`) provides a massive speedup by keeping string operations within C-level byte representations. Remember to escape `%` characters in JSON payloads as `%%`.
**Action:** Always pre-compute and encode static components to bytes outside of hot hashing loops, and use byte interpolation (`%`) along with hoisting external module function calls (like `hashlib.sha256`) to maximize inner-loop performance.
