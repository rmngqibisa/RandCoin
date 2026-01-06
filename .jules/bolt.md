# Bolt Journal

## 2024-05-24 - [Optimizing JSON Serialization in Mining Loop]
**Learning:** `json.dumps` is computationally expensive in tight loops (like Proof-of-Work mining). However, relying on key order with `sort_keys=True` can be brittle if hardcoded.
**Action:** Use string templating for static parts of the JSON and string concatenation for dynamic parts. Crucially, dynamically locate the injection point (e.g., using `.find()`) rather than hardcoding indices to ensure robustness against schema changes.
