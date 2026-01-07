## 2024-05-23 - [TOCTOU Vulnerability in Transaction Logic]
**Vulnerability:** Found a Time-of-Check to Time-of-Use (TOCTOU) vulnerability where a Transaction object could be validated by `Blockchain.add_transaction` but then modified in memory (e.g., changing amount to negative) before being mined into a block.
**Learning:** In local Python applications passing objects by reference, validation at the entry point is insufficient if the object remains mutable and accessible to the caller.
**Prevention:** Enforce immutability on critical financial data structures (like Transactions) using private attributes and properties, or deep copy objects upon crossing trust boundaries.

## 2024-05-24 - [Replay Attack Vulnerability in Transaction Processing]
**Vulnerability:** The `Blockchain.add_transaction` method did not check if a transaction ID had already been processed, allowing the same transaction to be added multiple times to the pending pool or blockchain (Replay Attack).
**Learning:** In simple blockchain implementations, relying solely on balance checks is insufficient for replay protection. Explicit checks against the ledger history are required.
**Prevention:** Implement a check against both the pending pool and the entire blockchain history (or a UTXO set/index) before accepting any new transaction.
