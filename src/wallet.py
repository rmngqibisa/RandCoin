import uuid
import hashlib

class Wallet:
    """
    Represents a simple wallet with an address.
    """
    def __init__(self):
        self.address = self.generate_address()

    def generate_address(self) -> str:
        """
        Generate a unique address based on a random UUID.
        """
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:16]

    def __repr__(self):
        return f"<Wallet Address: {self.address}>"
