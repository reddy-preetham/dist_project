from timeout import TimeoutInfo
from ledger import Ledger

import crypto_utils
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

class VoteMsg:
    def __init__(self, vote_info, ledger_commit_info, high_commit_qc, sender=a, signature=b): #need to update object variables
        self.vote_info = vote_info
        self.ledger_commit_info= ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        self.signature = signature

class QC:
    def __init__(self, vote_info, ledger_commit_info, signatures, author=a, author_signature=b): #need to update object variables
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = author
        self.author_signature = author_signature


class Block:
    def __init__(self, author, round, payload, qc, id):
        self.author = author
        self.round = round
        self.payload = payload
        self.qc = qc
        self.id = id


class BlockTree:
    high_qc
    high_commit_qc 
    def __int__(self, pending_votes, pending_block_tree): #not sure of instantiation
        self.pending_votes = pending_votes
        self.pending_block_tree = pending_block_tree
    def process_qc(self, qc):
        if qc.ledger_commit_info.commit_state_id != None:
            Ledger.commit(qc.vote_info.parent_id)
            pending_block_tree.prune(qc.vote_info.parent_id) #need to implement it
            high_commit_qc = max(qc, high_commit_qc)
        high_qc = max(qc, high_qc)

    def execute_and_insert(self, b):
        Ledger.speculate(b.qc.block_id,b.id, b.payload)
        self.pending_block_tree.add(b) #need to implement it

    def process_vote(self, v):
        self.process_qc(v.high_commit_qc)
        vote_idx = hash(v.ledger_commit_info)
        self.pending_votes[vote_idx].add(v.signature)
        if len(self.pending_votes[vote_idx])==2*f+1:
            qc = QC(v.vote_info, v.state_id, self.pending_votes[vote_idx])
            return qc
        return None

    def generate_blocks(self,txns, current_round):
        return Block(u, current_round, txns, high_qc, hash(author, current_round, txns, qc.vote_info.id, qc.signatures)) # need to implement it




        

