import unittest
import time
from main import Blockchain, Transaction, Block

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain(difficulty=1)
        self.miner_address = "Miner1"

    def test_genesis_block(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].previous_hash, "0")

    def test_transaction_serialization(self):
        tx = Transaction("A", "B", 10)
        self.assertEqual(tx.to_dict(), {'sender': 'A', 'recipient': 'B', 'amount': 10})

    def test_mining_and_rewards(self):
        self.blockchain.add_transaction(Transaction("Alice", "Bob", 10))
        self.blockchain.mine_pending_transactions(self.miner_address)

        # Chain length should increase
        self.assertEqual(len(self.blockchain.chain), 2)

        # Miner should have reward (10)
        self.assertEqual(self.blockchain.get_balance(self.miner_address), 10)

        # Alice sent 10, so balance -10 (assuming starting 0)
        self.assertEqual(self.blockchain.get_balance("Alice"), -10)
        self.assertEqual(self.blockchain.get_balance("Bob"), 10)

    def test_chain_validity(self):
        self.blockchain.add_transaction(Transaction("Alice", "Bob", 10))
        self.blockchain.mine_pending_transactions(self.miner_address)
        self.assertTrue(self.blockchain.is_chain_valid())

        # Tamper with the chain
        self.blockchain.chain[1].transactions[0].amount = 1000
        self.assertFalse(self.blockchain.is_chain_valid())

    def test_recalculate_hash_after_tamper(self):
        self.blockchain.add_transaction(Transaction("Alice", "Bob", 10))
        self.blockchain.mine_pending_transactions(self.miner_address)

        # Tamper
        self.blockchain.chain[1].transactions[0].amount = 1000
        # Even if we recalculate hash, it invalidates the link to next block (if there was one)
        # But here we check internal integrity (hash vs calculated hash)

        # The validation check checks:
        # 1. current_block.hash == calculated_hash
        # 2. current_block.previous_hash == previous_block.hash

        # By changing data, calculated_hash changes, so it won't match stored hash.
        self.assertFalse(self.blockchain.is_chain_valid())

        # If we update the hash, the previous_hash check of the *next* block would fail.
        # Let's mine another block to test chain linking
        self.blockchain.mine_pending_transactions(self.miner_address)
        self.assertEqual(len(self.blockchain.chain), 3)

        # Tamper block 1 again
        self.blockchain.chain[1].transactions[0].amount = 999
        self.assertFalse(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()
