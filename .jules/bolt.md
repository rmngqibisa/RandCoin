## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-05-23 - [O(N) Lookups in O(N) Loops]
**Learning:** Calculating spendable balance by iterating over all pending transactions (`sum(...)`) inside `add_transaction` creates an O(N^2) bottleneck.
**Action:** Maintain a running cache of pending outflows (`Dict[address, amount]`) that updates incrementally. This reduced the time to add 5000 transactions from ~3.1s to ~0.12s (25x speedup).

## 2024-05-24 - [Pre-sorting Dictionaries for JSON Serialization]
**Learning:** `json.dumps(..., sort_keys=True)` is O(N log N) overhead, and worse, it recursively sorts every sub-dictionary inside lists.
**Action:** Since Python 3.7+ preserves dictionary insertion order, instantiate dictionaries with keys pre-sorted alphabetically. This allows removing `sort_keys=True` entirely for significant speedups during serialization and hashing.
