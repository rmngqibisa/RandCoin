## 2024-05-22 - [JSON Serialization in Loops]
**Learning:** `json.dumps(..., sort_keys=True)` is incredibly expensive when called inside a tight loop like Proof of Work mining.
**Action:** For partial updates where only one key changes (and it's the first key), pre-compute the static suffix of the JSON string and use simple string concatenation. This yielded a ~6x speedup. Always verify that the key order assumption holds true.

## 2024-10-24 - [O(N^2) Transaction Validation]
**Learning:** Validating sender balance by iterating through `pending_transactions` creates an O(N^2) bottleneck when adding N transactions.
**Action:** Maintain a parallel `pending_outflows` cache (Dict[address, amount]) that updates on transaction addition and clears on mining. This reduced time for adding 5000 transactions from ~3.2s to ~0.25s (12x speedup).

## 2024-11-06 - [JSON String Formatting in Tight Loops]
**Learning:** Using byte template formatting (`b'...' % value`) inside tight loops like mining is ~10-15% faster than string concatenation followed by `.encode()`. However, `%` characters in payloads (e.g. JSON strings) must be explicitly escaped as `%%` to prevent format string vulnerabilities during the byte substitution step.
**Action:** When avoiding serialization in tight loops, pre-compute byte string templates with escaped `%` characters instead of repeatedly concatenating python strings and encoding them to bytes.
