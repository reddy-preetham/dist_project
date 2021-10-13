import nacl.encoding
import nacl.hash
from nacl.signing import SigningKey
from replica import *
HASHER = nacl.hash.sha256
def hash(msg):
    return HASHER(msg, encoder=nacl.encoding.HexEncoder)
def sign(record):
    return private_key.sign(hash(record))
