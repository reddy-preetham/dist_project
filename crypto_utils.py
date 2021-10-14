import nacl.encoding
import nacl.hash
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from replica import *

import pickle
# from replica import Replica
HASHER = nacl.hash.sha256
def hash(msg):
    return HASHER(pickle.dumps(msg))

def sign(record,key=Replica.private_key):
    return key.sign(pickle.dumps(record),encoder=HexEncoder)

def verify_decode(record,key):
    verify_key = VerifyKey(key, encoder=HexEncoder)
    verify_key.verify(record,encoder=HexEncoder)
    return pickle.loads(HexEncoder.decode(record.message))