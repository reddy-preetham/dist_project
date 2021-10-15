import nacl.encoding
import nacl.hash
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder

import pickle
# from replica import Replica

HASHER = nacl.hash.sha256
def hash(msg):
    return (HASHER(pickle.dumps(msg))).decode("utf-8") 

def sign(record,key):
    return key.sign(pickle.dumps(record),encoder=HexEncoder)

def verify_decode(record,key):
    verify_key = VerifyKey(key, encoder=HexEncoder)
    verify_key.verify(record,encoder=HexEncoder)
    return pickle.loads(HexEncoder.decode(record.message))

class Config:
    replica_id=""
    n_replicas=0
    n_faulty_replicas=0
    window_size=0
    exclude_size=0
    network_delta=0.0
    private_key=SigningKey.generate()
    public_key=private_key.verify_key.encode(encoder=HexEncoder)
    replica_pub_keys=[]




# class Block:
#     def __init__(self, author, round, payload, qc, id):
#         self.author = author
#         self.round = round
#         self.payload = payload
#         self.qc = qc
#         self.id = id
# genesis_block=Block()