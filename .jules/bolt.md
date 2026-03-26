## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-05-23 - [O(N) Lookups in O(N) Loops]
**Learning:** Calculating spendable balance by iterating over all pending transactions (`sum(...)`) inside `add_transaction` creates an O(N^2) bottleneck.
**Action:** Maintain a running cache of pending outflows (`Dict[address, amount]`) that updates incrementally. This reduced the time to add 5000 transactions from ~3.1s to ~0.12s (25x speedup).

## 2024-05-24 - [Avoid .encode() in Tight Loops]
**Learning:** String concatenation followed by `.encode()` inside tight loops (like Proof of Work) introduces unnecessary overhead. Using a pre-computed byte format template (e.g., `template % nonce`) skips the encoding step per iteration and speeds up execution significantly.
**Action:** When a loop generates strings just to encode them, pre-compute byte templates outside the loop. Remember to escape `%` characters in dynamic payloads using `.replace(b'%', b'%%')` to prevent format string vulnerabilities. Also, hoisting functions like `hashlib.sha256` reduces global lookup overhead.
