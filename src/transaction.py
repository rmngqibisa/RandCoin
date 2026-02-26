import hashlib
import json
import time
from decimal import Decimal
from typing import Dict, Any

class Transaction:
    """
    Represents a value transfer in the RandCoin network.
    Immutable to prevent tampering after creation/validation.
    """
    def __init__(self, sender: str, recipient: str, amount: Decimal, timestamp: float = None):
        """
        Initialize a new transaction.

        :param sender: The address of the sender.
        :param recipient: The address of the recipient.
        :param amount: The amount to send (in ZAR).
        :param timestamp: The time of creation.
        """
        if amount <= 0 and sender != "genesis":
            raise ValueError("Transaction amount must be positive.")
        if not sender:
            raise ValueError("Sender address cannot be empty.")
        if not recipient:
            raise ValueError("Recipient address cannot be empty.")

        # Use hidden attributes to simulate immutability with properties
        self._sender = sender
        self._recipient = recipient
        self._amount = amount
        self._timestamp = timestamp or time.time()
        self._id = self.calculate_hash()

        # Bolt Optimization: Cache the dictionary representation to avoid
        # repeated dictionary creation and float conversion during mining/validation.
        self._cached_dict = {
            "id": self._id,
            "sender": self._sender,
            "recipient": self._recipient,
            "amount": float(self._amount),
            "timestamp": self._timestamp
        }

    @property
    def sender(self) -> str:
        return self._sender

    @property
    def recipient(self) -> str:
        return self._recipient

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def id(self) -> str:
        return self._id

    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the transaction.
        """
        tx_content = {
            "sender": self._sender,
            "recipient": self._recipient,
            "amount": float(self._amount),  # Convert Decimal to float for JSON serialization compatibility
            "timestamp": self._timestamp
        }
        tx_string = json.dumps(tx_content, sort_keys=True).encode()
        return hashlib.sha256(tx_string).hexdigest()

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary.

        :param copy: Whether to return a copy or a direct reference.
        """
        if copy:
            return self._cached_dict.copy()
        return self._cached_dict

    def __repr__(self) -> str:
        return f"<Transaction {self._id[:8]}... {self._sender} -> {self._recipient}: {self._amount}>"
