from timeout import TC
# from timeout import TimeoutMsg
import safety as Safety
import block_tree as BlockTree
# import Broadcast

class Pacemaker:
    current_round=0
    last_round_tc=None
    pending_timeouts={}
    def __init__(self):
        pass
        
    def get_round_timer(cls, r): #need to implement this
        pass
    
    @classmethod
    def start_timer(cls, new_round):
        cls.stop_timer(cls.current_round) #need to implement stop_timer
        cls.current_round = new_round
        #start local timer for round current round for duration get round timer(current round)
    
    @classmethod
    def local_timeout_round(cls):
        timeout_info = Safety.make_timeout(cls.current_round, BlockTree.high_qc, cls.last_round_tc)
        #broadcast TimeoutMsg imeout info, last round tc, Block-Tree.high commit qcidont know how to implement it
    
    @classmethod
    def process_remote_timeout(cls, tmo): #need to remove f
        tmo_info = tmo.tmo_info
        if tmo_info.round<cls.current_round:
            return None

        cls.pending_votes.setdefault(tmo_info.round,set())
        if tmo_info.sender not in [x.sender for x in cls.pending_timeouts[tmo_info.round]]:
            cls.pending_timeouts[tmo_info.round].add(tmo_info)
        
        if len([x.sender for x in cls.pending_timeouts[tmo_info.round]]) == f+1:
            cls.stop_timer(cls.current_round)
            cls.local_timeout_round()
        if len([x.sender for x in cls.pending_timeouts[tmo_info.round]]) == 2*f+1:
            return TC(tmo_info.round, [x.high_qc_round for x in cls.pending_timeouts[tmo_info.round]], [x.signature for x in cls.pending_timeouts[tmo_info.round]])
        
        return None
    
    @classmethod
    def advance_round_tc(cls, tc):
        if tc==None or tc.round<cls.current_round:
            return False
        cls.last_round_tc = tc
        cls.start_timer(tc.round+1)
        return True
    
    @classmethod
    def advance_round_qc(cls, qc):
        if qc.vote_info.round < cls.current_round:
            return False
        cls.last_round_tc = None
        cls.start_timer(qc.vote_info.round+1)
        return True
    
        