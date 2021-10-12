import tc as TC
import safety as Safety
import block_tree as BlockTree
import Broadcast


class Pacemaker:
    def __init__(self):
        self.current_round = 0
        self.last_round_tc = None
        self.pending_timeouts = list()#what to initialize
        
    def get_round_timer(self, r):
        pass
    
    def start_timer(self, new_round):
        self.stop_timer(self.current_round) #need to implement stop_timer
        self.current_round = new_round
        #start local timer for round current round for duration get round timer(current round)
    
    def local_timeout_round(self):
        timeout_info = Safety.make_timeout(self.current_round, BlockTree.high_qc, self.last_round_tc)
        broadcast TimeoutMsg⟨timeout info, last round tc, Block-Tree.high commit qc⟩#idont know how to implement it
    
    def process_remote_timeout(self, tmo):
        tmo_info = tmo.tmo_info
        if tmo_info.round<self.current_round:
            return None
        if tmo_info.sender not in self.pending_timeouts[tmo_info.round].senders:
            self.pending_timeouts[tmo_info.round].add(tmo_info)
        
        if len(self.pending_timeouts[tmo_info.round].senders) == f+1:
            self.stop_timer(self.current_round)
            self.local_timeout_round()
        if len(self.pending_timeouts[tmo_info.round].senders) == 2*f+1:
            return TC(tmo_info.round, )#need to implement it
        
        return None
    
    def advance_round_tc(self, tc):
        if tc==None or len(tc)==0 or tc.round<self.current_round:
            return False
        self.last_round_tc = tc
        self.start_timer(tc.round+1)
        return True
    
    def advance_round_qc(self, qc):
        if qc.vote_info.round < self.current_round:
            return False
        self.last_round_tc = list()
        self.start_timer(qc.vote_info.round+1)
        return True
    
    def advance_round(self, qc):
        if qc.vote_info.round < self.current_round:
            return False
        self.last_round_tc = list()
        self.start_timer(qc.vote_info.round+1)
        return True
        
        