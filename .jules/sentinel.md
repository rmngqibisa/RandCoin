## 2024-05-24 - [Replay Attack Vulnerability]
**Vulnerability:** The blockchain implementation lacked a mechanism to check if a transaction had already been processed, allowing attackers to replay the same transaction object multiple times to drain funds.
**Learning:** In a distributed ledger, "state" is not just the current balance but the entire history of unique identifiers; validation must always include an existence check against this history.
**Prevention:** Implement a unique identifier (hash) for every state-changing command and enforce a strict "processed once" rule by maintaining a history of seen identifiers.
