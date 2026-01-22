from typing import List, Dict
from decimal import Decimal
from src.block import Block
from src.transaction import Transaction
from src.config import MINING_DIFFICULTY, MINING_REWARD, CURRENCY

class Blockchain:
    """
    Represents the RandCoin blockchain.
    """
    def __init__(self):
        """
        Initialize the blockchain.
        """
        self.chain: List[Block] = [self.create_genesis_block()]
        self.pending_transactions: List[Transaction] = []
        self.difficulty = MINING_DIFFICULTY
        self.balances: Dict[str, Decimal] = {}
        # Initialize balance cache with genesis block
        self._update_balance_from_block(self.chain[0])

    def _update_balance_from_block(self, block: Block):
        """
        Update the local balance cache based on transactions in the block.
        """
        for tx in block.transactions:
            # Credit recipient
            if tx.recipient not in self.balances:
                self.balances[tx.recipient] = Decimal(0)
            self.balances[tx.recipient] += tx.amount

            # Debit sender
            if tx.sender not in self.balances:
                self.balances[tx.sender] = Decimal(0)
            self.balances[tx.sender] -= tx.amount

    def create_genesis_block(self) -> Block:
        """
        Create the first block in the chain.
        """
        # Genesis transaction issues initial supply or just starts the chain
        return Block([Transaction("genesis", "system", Decimal(0))], "0")

    def get_latest_block(self) -> Block:
        """
        Get the latest block in the chain.
        """
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        """
        Add a transaction to the pending pool after validation.

        :param transaction: The transaction to add.
        :raises ValueError: If the transaction is invalid or funds are insufficient.
        """
        if transaction.amount <= 0:
            raise ValueError("Transaction amount must be positive.")

        # Verify Sender Balance (skip check for system/genesis)
        if transaction.sender not in ["genesis", "System"]:
            spendable_balance = self.get_spendable_balance(transaction.sender)
            if spendable_balance < transaction.amount:
                raise ValueError(f"Insufficient funds. Spendable Balance: {spendable_balance} {CURRENCY}, Required: {transaction.amount} {CURRENCY}")

        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        """
        Mine all pending transactions into a new block.

        :param miner_address: The address to receive the mining reward.
        """
        # Add a reward for the miner
        reward_tx = Transaction("System", miner_address, Decimal(MINING_REWARD))
        self.pending_transactions.append(reward_tx)

        new_block = Block(self.pending_transactions, self.get_latest_block().hash)
        new_block.mine(self.difficulty)

        self.chain.append(new_block)
        self._update_balance_from_block(new_block)
        self.pending_transactions = []

    def get_balance(self, address: str) -> Decimal:
        """
        Get the balance of an address from the local cache.

        :param address: The address to check.
        :return: The current balance.
        """
        return self.balances.get(address, Decimal(0))

    def get_spendable_balance(self, address: str) -> Decimal:
        """
        Get balance considering pending transactions.
        """
        balance = self.get_balance(address)
        pending_outgoing = sum(t.amount for t in self.pending_transactions if t.sender == address)
        return balance - pending_outgoing

    def is_chain_valid(self) -> bool:
        """
        Check if the blockchain is valid.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True
