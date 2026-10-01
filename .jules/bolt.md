## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-11-13 - [Byte format templating in Proof-of-Work loop]
**Learning:** String concatenation followed by `.encode()` in a tight loop is expensive. Pre-computing a byte template with `b'...'` and using Python byte-string formatting (e.g. `template % nonce`) avoids decoding/encoding overhead, leading to a ~25% speedup in Proof of Work mining over string formatting/concatenation.
**Action:** When rapidly changing a small numeric component of a large string that will be hashed, use byte string templating (`b'...' % val`). Be extremely careful to escape existing `%` symbols in the static payload with `b'%%'`.
