from pacemaker import Pacemaker
from block_tree import QC
import Ledger

class LeaderElection:
    def __init__(self):
        validators=
        window_size = 
        exclude_size = 
        reputation_leaders = map()
    
    def elect_reputation_leader(self, qc):
        active_validators = set()
        last_authors = set()
        current_qc = qc
        for :
            current_block = Ledger.committed_block(current_qc.vote_info.parent.parent_id)
            block_author = current_block.author
            if i<window_size:
                active_validators = set.union(active_validators, current_qc.signatures.signers())
            if(len(last_authors) < exclude_size):
                last_authors.add(block_author)
            current_qc = current_block.qc
        active_validators = active_validators-last_authors
        return #need to how to pick a random 
        
        
        
    def update_leaders(self, qc):
        extended_round = qc.vote_info.parent_round
        qc_round = qc.vote_info.round
        current_round = Pacemaker.current_round
        if extended_round+1 == qc_round and qc_round+1==current_round:
            self.reputation_leaders[current_round+1] = elect_repuation_leader(qc)
    
    def get_leader(self, round):
        if round in self.reputation_leaders:
            return self.reputation_leaders[round]
        return self.validators[math.floor(round/2)%len(self.validators)]
        