## 2024-05-23 - JSON Serialization Bottleneck in Mining
**Learning:** `json.dumps()` inside a tight loop is a massive performance killer, even with `sort_keys=True`. The overhead of serialization far outweighs the cost of SHA256 hashing.
**Action:** When a loop modifies only a single field (like a nonce), pre-compute the static parts of the string/bytes and use simple concatenation. This yielded a ~3.6x speedup (0.34s -> 0.09s).
