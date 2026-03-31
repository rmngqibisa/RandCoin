## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-05-23 - [O(N) Lookups in O(N) Loops]
**Learning:** Calculating spendable balance by iterating over all pending transactions (`sum(...)`) inside `add_transaction` creates an O(N^2) bottleneck.
**Action:** Maintain a running cache of pending outflows (`Dict[address, amount]`) that updates incrementally. This reduced the time to add 5000 transactions from ~3.1s to ~0.12s (25x speedup).

## 2025-03-19 - [String Formatting in Tight Loops]
**Learning:** Optimizing Python string concatenation to use byte format templates (`%b`) and localizing variable lookups (`hashlib.sha256`) inside the tight Proof of Work mining loop (`while` loop finding a hash) results in a measurable ~10-15% speedup.
**Action:** When working with high-frequency crypto loops in Python, switch to byte formatting (`template_bytes % b"%d"`) and hoist dot-accesses (e.g., `hashlib.sha256`) out of the loop.
