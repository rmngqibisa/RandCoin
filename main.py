class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
    
    def hash(self):
        # This is just a dummy hash function for demonstration purposes
        # A real cryptocurrency would use a more secure and complex hash function
        return hash((str(self.transactions) + str(self.previous_hash) + str(self.nonce)).encode())
    
    def mine(self, difficulty):
        # The mining process is simulated by incrementing the nonce until a hash with the desired number of leading zeros is found
        while self.hash()[:difficulty] != "0" * difficulty:
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = [Block([Transaction("genesis", "coinbase", 100)], "0")]
    
    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash()
        new_block = Block(transactions, previous_hash)
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
