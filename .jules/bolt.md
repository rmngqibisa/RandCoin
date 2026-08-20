## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-08-20 - Byte Formatting Optimization in Proof-of-Work Loop
**Learning:** In tight Python loops like a Proof-of-Work algorithm, repeatedly concatenating strings and then encoding to bytes (`str(nonce) + suffix).encode()`) is surprisingly expensive. Using a pre-computed byte template (`b'...' + b'%d' + b'...'`) and Python's byte string formatting (`%`) completely avoids string memory allocation and encoding overhead, speeding up the loop. Hoisting method lookups (`sha256 = hashlib.sha256`) out of the loop further enhances performance. However, when formatting byte templates that contain JSON payloads, any literal `%` signs inside the payload must be strictly escaped (replaced with `b'%%'`) to prevent `TypeError: not enough arguments for format string` format string vulnerability crashes.
**Action:** When optimizing tight iterative hashing loops, construct byte-level templates and use `%` formatting directly instead of building strings and calling `.encode()`. Always remember to escape `%` characters in dynamic byte payloads. Always hoist module function references outside the loop.
