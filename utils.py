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

def sign_record(record,key):
    # print(type(key))
    # print(("----------------------------------------------",pickle.dumps(record)))
    return key.sign(message=pickle.dumps(record),encoder=HexEncoder)

def verify_signature(record,key):
    verify_key = VerifyKey(key, encoder=HexEncoder)
    try:
        verify_key.verify(record,encoder=HexEncoder)
    except nacl.exceptions.BadSignatureError:
        # print("=========================",record,key)
        return False
    return True
    # return pickle.loads(HexEncoder.decode(record.message))
def validate_signatures(signatures_list):
    # return True
    for signature in signatures_list:
        is_valid=False
        for key in Config.replica_pub_keys.values():
            is_valid = is_valid or verify_signature(signature,key)
        if not is_valid:
            return False
    return True
def get_signers(signatures_list):
    signers=set()
    for signature in signatures_list:
        for key,value in Config.replica_pub_keys:
            if verify_signature(signature,value):
                signers.add(key)
                break
       
    return signers

class Config:
    replica_id=""
    n_replicas=0
    n_faulty_replicas=0
    window_size=0
    exclude_size=0
    network_delta=0.25
    private_key=SigningKey.generate()
    public_key=private_key.verify_key.encode(encoder=HexEncoder)
    replica_pub_keys=[]

    def set_config(replica_id,n_replicas,n_faulty_replicas,window_size,network_delta,public_key,private_key,replica_public_keys):
        Config.replica_id = replica_id
        Config.n_replicas = n_replicas
        Config.n_faulty_replicas = n_faulty_replicas
        Config.window_size = window_size
        Config.network_delta = network_delta
        Config.public_key=public_key
        Config.private_key=private_key
        Config.replica_pub_keys=replica_public_keys



# class Block:
#     def __init__(self, author, round, payload, qc, id):
#         self.author = author
#         self.round = round
#         self.payload = payload
#         self.qc = qc
#         self.id = id
# genesis_block=Block()