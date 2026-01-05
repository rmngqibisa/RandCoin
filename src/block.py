import hashlib
import json
import time
from typing import List
from src.transaction import Transaction

class Block:
    """
    Represents a block in the RandCoin blockchain.
    """
    def __init__(self, transactions: List[Transaction], previous_hash: str, timestamp: float = None):
        """
        Initialize a new block.

        :param transactions: List of transactions in the block.
        :param previous_hash: Hash of the previous block.
        :param timestamp: Creation timestamp.
        """
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the block.
        """
        block_content = {
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }
        # Sort keys to ensure consistent hashing
        block_string = json.dumps(block_content, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine(self, difficulty: int):
        """
        Mine the block by finding a nonce that satisfies the difficulty.

        :param difficulty: Number of leading zeros required in the hash.
        """
        target = "0" * difficulty

        # Optimization: Pre-compute the dict representation of transactions
        # This avoids re-converting transactions to dicts and floats in every iteration
        # of the mining loop, while keeping calculate_hash() pure for verification.
        tx_list = [t.to_dict() for t in self.transactions]

        block_content = {
            "transactions": tx_list,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }

        while self.hash[:difficulty] != target:
            self.nonce += 1

            # Update nonce in the content
            block_content["nonce"] = self.nonce

            # Re-serialize. Note: In Python's json, sort_keys=True ensures consistent order.
            # Since we constructed block_content with the same structure as calculate_hash,
            # this produces the same string.
            block_string = json.dumps(block_content, sort_keys=True).encode()

            self.hash = hashlib.sha256(block_string).hexdigest()
