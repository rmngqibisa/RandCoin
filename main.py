import sys
from decimal import Decimal, InvalidOperation
from src.blockchain import Blockchain
from src.transaction import Transaction
from src.wallet import Wallet
from src.config import CURRENCY

def main():
    print("Welcome to RandCoin! (Linked to ZAR)")
    blockchain = Blockchain()

    # Create a default wallet for the user (simulation)
    my_wallet = Wallet()
    print(f"Your Wallet Address: {my_wallet.address}")

    while True:
        print("\n=== RandCoin Menu ===")
        print("1. View Blockchain")
        print("2. Create Transaction")
        print("3. Mine Pending Transactions")
        print("4. Check Balance")
        print("5. Verify Chain Integrity")
        print("6. Generate New Wallet")
        print("7. Exit")

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
            sender = input("Sender (leave blank for your wallet): ").strip()
            if not sender:
                sender = my_wallet.address

            recipient = input("Recipient: ").strip()
            try:
                amount_str = input(f"Amount ({CURRENCY}): ")
                amount = Decimal(amount_str)

                # Check for overdraft before adding (double check in UI)
                blockchain.add_transaction(Transaction(sender, recipient, amount))
                print("Transaction added to pool.")
            except InvalidOperation:
                print("Error: Invalid amount format.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            miner_address = input("Enter miner address (leave blank for your wallet): ").strip()
            if not miner_address:
                miner_address = my_wallet.address

            print("Mining...")
            blockchain.mine_pending_transactions(miner_address)
            print("Block successfully mined!")

        elif choice == '4':
            address = input("Address (leave blank for your wallet): ").strip()
            if not address:
                address = my_wallet.address

            balance = blockchain.get_balance(address)
            print(f"Balance of {address}: {balance} {CURRENCY}")

        elif choice == '5':
            if blockchain.is_chain_valid():
                print("Blockchain is valid.")
            else:
                print("Blockchain is NOT valid!")

        elif choice == '6':
            my_wallet = Wallet()
            print(f"New Wallet Generated: {my_wallet.address}")

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
