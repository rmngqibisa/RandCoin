## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2026-10-15 - Fast JSON Serialization to Byte Format Templates
**Learning:** In tight proof-of-work mining loops, constructing strings for hashing using concatenation and then calling `.encode()` introduces significant overhead. Pre-computing a byte format template (`b'{"nonce": %d...}'`) and replacing the percent symbol for escaping (`b'%%'`) inside strings, along with hoisting functions like `hashlib.sha256` out of the loop, drastically reduces latency per iteration.
**Action:** Use byte formatting directly (e.g. `template % nonce`) inside the loop, and safely escape data placeholders when adapting JSON into these byte templates to avoid format string errors. Hoist variable lookups.
