## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-11-20 - [Byte Format Templates in Proof of Work]
**Learning:** In very hot loops like Proof of Work mining, string concatenation and `.encode()` combined take up significant overhead. Additionally, manual field extraction instead of utilizing optimized object properties (`t.to_dict(copy=False)`) breaks encapsulation and can lead to precision loss (e.g. Decimal to float casting risks).
**Action:** Use byte format templates (`b'{"nonce": %d' + suffix_bytes`) to completely eliminate `.encode()` in the loop. Always use `.replace(b'%', b'%%')` to escape `%` in the suffix to avoid format string errors. Ensure you don't inline object serialization manually; always use the object's provided methods to maintain encapsulation.
