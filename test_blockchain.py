import unittest
from decimal import Decimal
from src.blockchain import Blockchain
from src.transaction import Transaction

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        # Reduce difficulty for testing speed
        self.blockchain.difficulty = 1
        self.miner_address = "Miner1"
        self.alice = "Alice"
        self.bob = "Bob"

    def test_genesis_block(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].previous_hash, "0")

    def test_transaction_serialization(self):
        tx = Transaction("A", "B", Decimal("10.5"))
        # Check dict structure
        data = tx.to_dict()
        self.assertEqual(data['sender'], 'A')
        self.assertEqual(data['recipient'], 'B')
        self.assertEqual(data['amount'], 10.5)

    def test_mining_and_rewards(self):
        # Initial state: Miner has 0
        self.assertEqual(self.blockchain.get_balance(self.miner_address), Decimal(0))

        # Mine a block to get rewards (since no transactions are pending yet)
        self.blockchain.mine_pending_transactions(self.miner_address)

        # Chain length should be 2
        self.assertEqual(len(self.blockchain.chain), 2)

        # Miner should have reward (10)
        self.assertEqual(self.blockchain.get_balance(self.miner_address), Decimal(10))

    def test_balance_check_and_transfer(self):
        # Alice tries to send money she doesn't have
        with self.assertRaises(ValueError):
            self.blockchain.add_transaction(Transaction(self.alice, self.bob, Decimal(10)))

        # Mine some coins for Alice
        self.blockchain.mine_pending_transactions(self.alice) # Alice gets 10
        self.assertEqual(self.blockchain.get_balance(self.alice), Decimal(10))

        # Now Alice sends 5 to Bob
        self.blockchain.add_transaction(Transaction(self.alice, self.bob, Decimal(5)))

        # Balance shouldn't change until mined (except spendable check prevents double spend)
        # Check spendable balance
        self.assertEqual(self.blockchain.get_spendable_balance(self.alice), Decimal(5))

        # Mine the transaction
        self.blockchain.mine_pending_transactions(self.miner_address)

        # Alice: 10 (reward) - 5 (sent) = 5
        self.assertEqual(self.blockchain.get_balance(self.alice), Decimal(5))
        # Bob: 5 (received)
        self.assertEqual(self.blockchain.get_balance(self.bob), Decimal(5))
        # Miner: 10 (reward)
        self.assertEqual(self.blockchain.get_balance(self.miner_address), Decimal(10))

    def test_chain_validity(self):
        # Mine a block
        self.blockchain.mine_pending_transactions(self.miner_address)
        self.assertTrue(self.blockchain.is_chain_valid())

        # Tamper with the chain
        # Change amount of reward transaction in block 1
        self.blockchain.chain[1].transactions[0].amount = Decimal(1000)
        self.assertFalse(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()
