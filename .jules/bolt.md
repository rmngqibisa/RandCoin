## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-05-30 - Proof of Work Mining Loop Optimization
**Learning:** String concatenation and `json.dumps()` in Python's inner mining loop is a significant bottleneck. Using byte-string templating (e.g. `b'{"nonce": %d' + suffix_bytes`) and escaping formatting characters (e.g. `replace(b'%', b'%%')`) avoids repeated `.encode()` calls and strings parsing, and dramatically speeds up operations. Furthermore, hoisting global variable lookups (e.g. `sha256 = hashlib.sha256`) out of the tight `while` loop yields a non-trivial performance boost.
**Action:** When optimizing tight inner loops in Python (like Proof of Work hashing), prefer pre-computing byte strings, using byte interpolation (`%`), avoiding redundant object creation/encoding, and hoisting global/attribute lookups to local variables.
