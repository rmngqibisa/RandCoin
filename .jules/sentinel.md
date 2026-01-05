## 2024-05-23 - [TOCTOU Vulnerability in Transaction Logic]
**Vulnerability:** Found a Time-of-Check to Time-of-Use (TOCTOU) vulnerability where a Transaction object could be validated by `Blockchain.add_transaction` but then modified in memory (e.g., changing amount to negative) before being mined into a block.
**Learning:** In local Python applications passing objects by reference, validation at the entry point is insufficient if the object remains mutable and accessible to the caller.
**Prevention:** Enforce immutability on critical financial data structures (like Transactions) using private attributes and properties, or deep copy objects upon crossing trust boundaries.
