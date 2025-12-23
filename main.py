import hashlib
import json
import time
from typing import List, Dict, Any

class Transaction:
    """
    Represents a transaction in the blockchain.
    """
    def __init__(self, sender: str, recipient: str, amount: float):
        """
        Initialize a new transaction.

        :param sender: The address of the sender.
        :param recipient: The address of the recipient.
        :param amount: The amount to send.
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary.

        :return: Dictionary representation of the transaction.
        """
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }

    def __repr__(self) -> str:
        return str(self.to_dict())

class Block:
    """
    Represents a block in the blockchain.
    """
    def __init__(self, transactions: List[Transaction], previous_hash: str, timestamp: float = None):
        """
        Initialize a new block.

        :param transactions: List of transactions in the block.
        :param previous_hash: Hash of the previous block.
        :param timestamp: Creation timestamp (defaults to current time).
        """
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the block.

        :return: Hex string of the hash.
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
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    """
    Represents the blockchain itself.
    """
    def __init__(self, difficulty: int = 2):
        """
        Initialize the blockchain.

        :param difficulty: Mining difficulty (number of leading zeros).
        """
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        """
        Create the first block in the chain.

        :return: The genesis block.
        """
        return Block([Transaction("genesis", "coinbase", 0)], "0")

    def get_latest_block(self) -> Block:
        """
        Get the latest block in the chain.

        :return: The last Block object.
        """
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        """
        Add a transaction to the pending pool.

        :param transaction: The transaction to add.
        :raises ValueError: If the amount is invalid.
        """
        if transaction.amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self, miner_address: str):
        """
        Mine all pending transactions into a new block.

        :param miner_address: The address to receive the mining reward.
        """
        # Add a reward for the miner
        reward_tx = Transaction("System", miner_address, 10)
        self.pending_transactions.append(reward_tx)

        new_block = Block(self.pending_transactions, self.get_latest_block().hash)
        new_block.mine(self.difficulty)

        print("Block successfully mined!")
        self.chain.append(new_block)

        self.pending_transactions = []

    def get_balance(self, address: str) -> float:
        """
        Calculate the balance of an address by iterating through the chain.

        :param address: The address to check.
        :return: The current balance.
        """
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
        return balance

    def is_chain_valid(self) -> bool:
        """
        Check if the blockchain is valid.

        :return: True if valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                print("Current hash is invalid")
                return False

            if current_block.previous_hash != previous_block.hash:
                print("Previous hash is invalid")
                return False
        return True

def main():
    print("Welcome to RandCoin!")
    difficulty = 2
    blockchain = Blockchain(difficulty)

    miner_address = input("Enter your wallet address (to receive mining rewards): ")

    while True:
        print("\nMenu:")
        print("1. View Blockchain")
        print("2. Create Transaction")
        print("3. Mine Pending Transactions")
        print("4. Check Balance")
        print("5. Verify Chain Integrity")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            for block in blockchain.chain:
                print("-------------------------")
                print(f"Index: {blockchain.chain.index(block)}")
                print(f"Timestamp: {block.timestamp}")
                print(f"Transactions: {block.transactions}")
                print(f"Previous Hash: {block.previous_hash}")
                print(f"Hash: {block.hash}")
                print("-------------------------")

        elif choice == '2':
            sender = input("Sender: ")
            recipient = input("Recipient: ")
            try:
                amount = float(input("Amount: "))
                blockchain.add_transaction(Transaction(sender, recipient, amount))
                print("Transaction added to pool.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            print("Mining...")
            blockchain.mine_pending_transactions(miner_address)

        elif choice == '4':
            address = input("Address: ")
            print(f"Balance of {address}: {blockchain.get_balance(address)}")

        elif choice == '5':
            if blockchain.is_chain_valid():
                print("Blockchain is valid.")
            else:
                print("Blockchain is NOT valid!")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
