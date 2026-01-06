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

        # Optimization: Pre-compute string parts for faster serialization
        # This avoids calling json.dumps in the mining loop, which is a major bottleneck.
        # We construct the JSON string manually by updating only the nonce part.

        # Create a template with a known nonce (0) to find the split point
        temp_content = block_content.copy()
        temp_content["nonce"] = 0
        temp_string = json.dumps(temp_content, sort_keys=True)

        # Locate the "nonce": 0 substring to split the string.
        # This makes the optimization robust even if key order changes (e.g. if new fields are added).
        nonce_marker = '"nonce": 0'
        split_index = temp_string.find(nonce_marker)

        if split_index == -1:
            # Fallback if JSON format is unexpected
            prefix = None
            suffix = None
        else:
            # Prefix includes up to '"nonce": '
            # len('"nonce": ') is 9
            prefix = temp_string[:split_index + 9]
            # Suffix starts after the '0'
            suffix = temp_string[split_index + len(nonce_marker):]

        while self.hash[:difficulty] != target:
            self.nonce += 1

            if prefix:
                # Fast path: manual string construction
                block_string = (prefix + str(self.nonce) + suffix).encode()
            else:
                # Slow path: full serialization
                block_content["nonce"] = self.nonce
                block_string = json.dumps(block_content, sort_keys=True).encode()

            self.hash = hashlib.sha256(block_string).hexdigest()
