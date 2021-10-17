from utils import *
class VoteInfo:
    def __init__(self, id, round, parent_id, parent_round, state):
        self.id = id
        self.round = round
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.state = state
    
class LedgerCommitInfo:
    def __init__(self, commit_state_id, vote_info_hash):
        self.commit_state_id = commit_state_id
        self.vote_info_hash = vote_info_hash
    
    def to_string(self):
        return "" + self.commit_state_id + self.vote_info_hash

class VoteMsg:
    def __init__(self, vote_info, ledger_commit_info, high_commit_qc): #need to update object variables
        self.vote_info = vote_info
        self.ledger_commit_info= ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = Config.replica_id
        self.signature = sign_record(self.ledger_commit_info,Config.private_key).decode("utf-8") 

class QC:
    def __init__(self, vote_info, ledger_commit_info, signatures): #need to update object variables
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = Config.replica_id        
        self.author_signature = sign_record(self.signatures,Config.private_key).decode("utf-8") 
        

class Block:
    def __init__(self, author, round, payload, qc, id):
        self.author = author
        self.round = round
        self.payload = payload
        self.qc = qc
        self.id = id