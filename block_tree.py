# from timeout import TimeoutInfo
from ledger import Ledger
from crypto_utils import *
from replica import *
import crypto_utils
from block import *

class VoteInfo:
    def __init__(self, id, round, parent_id, parent_round, state):
        self.id = id
        self.round = round
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.state = state
    
class LedgerCommitInfo:
    def __init__(self, id, vote):
        self.commit_state_id = id
        self.vote_info_hash = vote
    
    def to_string(self):
        return "" + self.commit_state_id + self.vote_info_hash

class VoteMsg:
    def __init__(self, vote_info, ledger_commit_info, high_commit_qc): #need to update object variables
        self.vote_info = vote_info
        self.ledger_commit_info= ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = name
        self.signature = sign(self.ledger_commit_info.to_string())

class QC:
    def __init__(self, vote_info, ledger_commit_info, signatures): #need to update object variables
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = name
        self.author_signature = sign("".join(self.signatures))


    def to_string(self):
        return hash("".join(self.vote_info).join(self.ledger_commit_info.to_string()).join(self.signatures).join(self.author).join(self.author_signature))



class Block:
    def __init__(self, author, round, payload, qc, id):
        self.author = author
        self.round = round
        self.payload = payload
        self.qc = qc
        self.id = id


class BlockTree:
    high_qc=0
    high_commit_qc=0 
    pending_votes={}#wrong implementation
    pending_block_tree= Tree() #wrong implementation
    # genesis_block=Block()

    # def __int__(self, pending_votes, pending_block_tree): #not sure of instantiation
    #     self.pending_votes = pending_votes
    #     self.pending_block_tree = pending_block_tree

    def __init__(self):
        pass

    def process_qc(cls, qc):
        if qc.ledger_commit_info.commit_state_id != None:
            Ledger.commit(qc.vote_info.parent_id)
            cls.pending_block_tree.prune(qc.vote_info.parent_id) #need to implement it
            cls.high_commit_qc = max(qc, cls.high_commit_qc)
        cls.high_qc = max(qc, cls.high_qc)

    def execute_and_insert(cls, b):
        Ledger.speculate(b.qc.block_id,b.id, b.payload)
        cls.pending_block_tree.add(b) #need to implement it

    def process_vote(cls, v):
        cls.process_qc(v.high_commit_qc)
        vote_idx = hash(v.ledger_commit_info.to_string())
        cls.pending_votes.setdefault(vote_idx,set())
        cls.pending_votes[vote_idx].add(v.signature)
        if len(cls.pending_votes[vote_idx])==2*f+1:
            qc = QC(v.vote_info, v.state_id, cls.pending_votes[vote_idx])
            return qc
        return None

    def generate_blocks(cls,txns, current_round):
        return Block(name, current_round, txns, cls.high_qc, hash("".join(name).join(current_round).join(txns).join(cls.high_qc.vote_info.id).join(cls.high_qc.signatures))) # need to implement it


        

