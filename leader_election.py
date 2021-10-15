from pacemaker import Pacemaker
# from block_tree import QC
# from ledger import Ledger
import math
import random

class LeaderElection:
    def __init__(self): #need to know constructors
        self.validators= list()
        self.window_size = 0    #need to initialize 
        self.exclude_size = 0   #need to initialize 
        self.reputation_leaders = dict()
    
    def elect_reputation_leader(self, qc):
        active_validators = set()
        last_authors = set()
        current_qc = qc
        curr_window_size=0
        while(curr_window_size<self.window_size or len(last_authors)<self.exclude_size):
            current_block = Ledger.committed_block(current_qc.vote_info.parent_id)
            block_author = current_block.author
            if curr_window_size<self.window_size:
                active_validators = set.union(active_validators, current_qc.signatures.signers())
            if(len(last_authors) < self.exclude_size):
                last_authors.add(block_author)
            current_qc = current_block.qc
            curr_window_size+=1
        active_validators = active_validators-last_authors
        random.seed(10)
        return random.choice(active_validators)
        
    def update_leaders(self, qc):
        extended_round = qc.vote_info.parent_round
        qc_round = qc.vote_info.round
        current_round = Pacemaker.current_round
        if extended_round+1 == qc_round and qc_round+1==current_round:
            self.reputation_leaders[current_round+1] = self.elect_repuation_leader(qc)
    
    def get_leader(self, round):
        if round in self.reputation_leaders:
            return self.reputation_leaders[round]
        return self.validators[math.floor(round/2)%len(self.validators)]
        