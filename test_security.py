import unittest
from decimal import Decimal
from src.transaction import Transaction
from src.blockchain import Blockchain

class TestTransactionSecurity(unittest.TestCase):
    def test_immutability(self):
        """
        Verify that transaction attributes cannot be modified after creation.
        This prevents TOCTOU (Time-of-Check to Time-of-Use) attacks.
        """
        tx = Transaction("Alice", "Bob", Decimal(10))

        # Try to modify amount
        with self.assertRaises(AttributeError):
            tx.amount = Decimal(1000)

        # Try to modify sender
        with self.assertRaises(AttributeError):
            tx.sender = "Mallory"

        # Try to modify recipient
        with self.assertRaises(AttributeError):
            tx.recipient = "Mallory"

    def test_validation(self):
        """
        Verify that invalid transactions cannot be created.
        """
        # Negative amount
        with self.assertRaises(ValueError):
            Transaction("Alice", "Bob", Decimal(-10))

        # Zero amount (non-genesis)
        with self.assertRaises(ValueError):
            Transaction("Alice", "Bob", Decimal(0))

        # Empty sender
        with self.assertRaises(ValueError):
            Transaction("", "Bob", Decimal(10))

        # Empty recipient
        with self.assertRaises(ValueError):
            Transaction("Alice", "", Decimal(10))

    def test_replay_protection(self):
        """
        Verify that the same transaction cannot be added twice (Replay Protection).
        """
        bc = Blockchain()
        # Create a valid transaction. Use "System" to skip balance check, focusing on replay logic.
        tx = Transaction("System", "Alice", Decimal(10))

        bc.add_transaction(tx)

        # Try to add the exact same transaction object again
        with self.assertRaisesRegex(ValueError, "Transaction already exists"):
            bc.add_transaction(tx)

if __name__ == '__main__':
    unittest.main()
