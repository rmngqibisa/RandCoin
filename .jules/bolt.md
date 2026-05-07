## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-10-25 - [Byte Templating in Proof of Work]
**Learning:** String concatenation and `.encode()` within the tight Proof of Work mining loop (`mine` in `src/block.py`) incur unnecessary overhead. By pre-computing a byte template (`b'%d'`) and substituting the nonce with byte string formatting, along with hoisting `hashlib.sha256` to a local variable, performance can be improved by roughly 10-15%. However, it's crucial to escape any existing `%` characters in the JSON payload (using `replace(b'%', b'%%')`) to prevent format string bugs.
**Action:** When optimizing tight loops involving hashing and strings, use byte templates and local variable hoisting, ensuring proper escaping of format string characters.
