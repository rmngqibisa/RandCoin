import time
import hashlib

def old_way(iterations):
    prefix = '{"nonce": '
    suffix = ', "previous_hash": "0000abc", "timestamp": 12345.67, "transactions": []}'
    target = "000"
    nonce = 0
    h = ""
    start = time.time()
    for _ in range(iterations):
        nonce += 1
        block_string = (prefix + str(nonce) + suffix).encode()
        h = hashlib.sha256(block_string).hexdigest()
    print("Old way:", time.time() - start)

def new_way(iterations):
    suffix = ', "previous_hash": "0000abc", "timestamp": 12345.67, "transactions": []}'
    suffix_bytes = suffix.replace('%', '%%').encode()
    template = b'{"nonce": %d' + suffix_bytes
    sha256 = hashlib.sha256
    target = "000"
    nonce = 0
    h = ""
    start = time.time()
    for _ in range(iterations):
        nonce += 1
        block_string = template % nonce
        h = sha256(block_string).hexdigest()
    print("New way:", time.time() - start)

old_way(100000)
new_way(100000)
