## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).
## 2026-09-10 - Proof of Work Loop Byte Templating and Key Ordering Fix
**Learning:** Python string formatting with `b"..." % nonce` is significantly faster than using `.encode()` inside a tight `while` loop (like Proof of Work). Also, manually ordering dictionary keys to simulate `sort_keys=True` requires being very careful about duplicate keys; if duplicate keys exist in the dict literal, the order may not be exactly as written, which can break JSON string hashes and invalidating the blockchain.
**Action:** When optimizing loop bottlenecks involving string processing and encoding, try to move `.encode()` outside the loop and use byte string formatting. Also, always verify dictionary keys are unique when manually guaranteeing order.
