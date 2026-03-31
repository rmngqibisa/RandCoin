## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2026-02-12 - [List Scans in Validation Hot Paths]
**Learning:** Iterating over `pending_transactions` to sum outflows for every `add_transaction` call creates an O(N^2) bottleneck, degrading performance as the mempool grows.
**Action:** Maintain a parallel `pending_outflows` cache (Map<Address, Amount>) that is updated on transaction addition (O(1)) and cleared on mining. This reduced validation time for 4000 transactions from ~2s to ~0.08s (24x speedup).
