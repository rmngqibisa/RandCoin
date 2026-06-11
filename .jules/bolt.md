## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).
## 2024-10-25 - [Byte Templating in Tight Hash Loops]
**Learning:** In Proof-of-Work mining loops, repeated string concatenation and `.encode()` calls are expensive. Furthermore, `template_bytes % b1.nonce` is slower than `template_bytes % nonce` (due to attribute lookup overhead).
**Action:** Pre-encode the static parts of the string into a byte template using `%d`, safely escape `%` via `.replace('%', '%%')`, and hoist attribute lookups (`self.nonce`, `self.hash`) to local variables (`nonce`, `h`) outside the loop. This shaves another ~10% off raw hashing time compared to string concatenation.
