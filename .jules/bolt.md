## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2026-09-03 - [Proof of Work Mining Optimization with Byte Formatting]
**Learning:** In very hot loops (like PoW mining), constructing strings (`prefix + str(nonce) + suffix`) and then `.encode()`ing them each iteration is still a bottleneck. Using C-level byte string formatting (`template % nonce` where template is a pre-encoded bytes object) and hoisting global functions (like `hashlib.sha256`) out of the loop provides significant speedups.
**Action:** When working in ultra-high frequency loops generating byte-level hashes, pre-compute byte string templates with placeholders and use Python's `%` formatting on bytes. Ensure any user data in the template is safely escaped (`replace(b'%', b'%%')`) to avoid format string vulnerabilities.
