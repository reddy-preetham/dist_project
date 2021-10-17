import nacl.encoding
import nacl.hash
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
import pickle

HASHER = nacl.hash.sha256


class Config:
    replica_id = ""
    n_replicas = 0
    window_size = 0
    private_key = SigningKey.generate()
    replica_pub_keys = []


def hash(msg):
    """Returns string representation hash of object msg"""
    return (HASHER(pickle.dumps(msg))).decode("utf-8")


def sign_record(record, key):
    """Signs and returns signature of a record with a private key"""
    return key.sign(message=pickle.dumps(record), encoder=HexEncoder)


def verify_signature(signature, key):
    """Verifies signature with a public key"""
    verify_key = VerifyKey(key, encoder=HexEncoder)
    try:
        verify_key.verify(signature, encoder=HexEncoder)
    except nacl.exceptions.BadSignatureError:
        return False
    return True


def validate_signatures(signatures_list):
    """Validates signatures in signature list with replica public keys
    and returns True if the signature can be vaidated by
    any of the replica public key.
    """
    for signature in signatures_list:
        is_valid = False
        for key in Config.replica_pub_keys.values():
            is_valid = is_valid or verify_signature(signature, key)
        if not is_valid:
            return False
    return True


def get_signers(signatures_list):
    """Returns set of signers (replica ids) of signatures
    in the signature list
    """
    signers = set()
    for signature in signatures_list:
        for key, value in Config.replica_pub_keys:
            if verify_signature(signature, value):
                signers.add(key)
                break
    return signers
