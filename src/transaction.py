import hashlib
import json
import time
from decimal import Decimal
from typing import Dict, Any

class Transaction:
    """
    Represents a value transfer in the RandCoin network.
    """
    def __init__(self, sender: str, recipient: str, amount: Decimal, timestamp: float = None):
        """
        Initialize a new transaction.

        :param sender: The address of the sender.
        :param recipient: The address of the recipient.
        :param amount: The amount to send (in ZAR).
        :param timestamp: The time of creation.
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.id = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the transaction.
        """
        tx_content = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": float(self.amount),  # Convert Decimal to float for JSON serialization compatibility
            "timestamp": self.timestamp
        }
        tx_string = json.dumps(tx_content, sort_keys=True).encode()
        return hashlib.sha256(tx_string).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary.
        """
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": float(self.amount),
            "timestamp": self.timestamp
        }

    def __repr__(self) -> str:
        return f"<Transaction {self.id[:8]}... {self.sender} -> {self.recipient}: {self.amount}>"
