## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).
## 2024-07-09 - Avoid .encode() in Hot Hash Loops
**Learning:** In proof-of-work mining loops, calling `.encode()` on strings inside the loop introduces significant overhead. Pre-encoding strings into byte templates and using byte formatting (`%b` or `%d`) yields an extra speedup. When doing this with JSON payloads, any `%` characters must be strictly escaped as `%%` to prevent format string bugs or crashes.
**Action:** Use byte string templates for repetitive string-to-bytes operations in hot loops. Pre-encode static sections and dynamically inject changing values directly into bytes.
