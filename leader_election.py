from pacemaker import Pacemaker
from utils import *
import math
import random

class LeaderElection:
    validators= list()
    window_size = Config.window_size   
    exclude_size = Config.exclude_size
    reputation_leaders = dict()
    
    @classmethod
    def elect_reputation_leader(cls, qc):
        active_validators = set()
        last_authors = set()
        current_qc = qc
        curr_window_size=0
        while(curr_window_size<cls.window_size or len(last_authors)<cls.exclude_size):
            current_block = Ledger.committed_block(current_qc.vote_info.parent_id)
            block_author = current_block.author
            if curr_window_size<cls.window_size:
                active_validators = set.union(active_validators, current_qc.signatures.signers())
            if(len(last_authors) < cls.exclude_size):
                last_authors.add(block_author)
            current_qc = current_block.qc
            curr_window_size+=1
        active_validators = active_validators-last_authors
        random.seed(qc.vote_info.round)
        return random.choice(active_validators)

    @classmethod    
    def update_leaders(cls, qc):
        extended_round = qc.vote_info.parent_round
        qc_round = qc.vote_info.round
        current_round = Pacemaker.current_round
        if extended_round+1 == qc_round and qc_round+1==current_round:
            cls.reputation_leaders[current_round+1] = cls.elect_repuation_leader(qc)
    
    @classmethod
    def get_leader(cls, round):
        if round in cls.reputation_leaders:
            return cls.reputation_leaders[round]
        return cls.validators[math.floor(round/2)%len(cls.validators)]
        