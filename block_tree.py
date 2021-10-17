# from timeout import TimeoutInfo
from ledger import Ledger
from utils import *
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
        self.sender = Config.replica_id
        self.signature = sign(self.ledger_commit_info,Config.private_key)

class QC:
    def __init__(self, vote_info, ledger_commit_info, signatures): #need to update object variables
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = Config.replica_id
        self.author_signature = sign("".join(self.signatures),Config.private_key)


    # def to_string(self):
    #     return hash("".join(self.vote_info).join(self.ledger_commit_info.to_string()).join(self.signatures).join(self.author).join(self.author_signature))



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
    pending_votes={}
    genesis_block=Block(Config.replica_id, -1, [], -1, hash("".join(Config.replica_id).join(-1).join([]).join(-1).join([])))
    pending_block_tree= Tree(genesis_block) 


    def __init__(self):
        pass

    def process_qc(cls, qc):
        if qc.ledger_commit_info.commit_state_id != None:
            Ledger.commit(cls.pending_block_tree.get_block(qc.vote_info.parent_id))
            cls.pending_block_tree.prune(qc.vote_info.parent_id) #need to implement it
            cls.high_commit_qc = max(qc.vote_info.round, cls.high_commit_qc.vote_info.round)
        cls.high_qc = max(qc.vote_info.round, cls.high_qc.vote_info.round)

    def execute_and_insert(cls, b):
        Ledger.speculate(b.qc.block_id,b)
        cls.pending_block_tree.add(b) 

    def process_vote(cls, v):
        cls.process_qc(v.high_commit_qc)
        vote_idx = hash(v.ledger_commit_info)
        cls.pending_votes.setdefault(vote_idx,set())
        cls.pending_votes[vote_idx].add(v.signature)
        if len(cls.pending_votes[vote_idx])==2*Config.n_faulty_replicas+1:
            qc = QC(v.vote_info, v.state_id, list(cls.pending_votes[vote_idx]))
            return qc
        return None

    def generate_blocks(cls,txns, current_round):
        return Block(Config.replica_id, current_round, txns, cls.high_qc, hash("".join(Config.replica_id).join(current_round).join(txns).join(cls.high_qc.vote_info.id).join(cls.high_qc.signatures))) # need to implement it


        

