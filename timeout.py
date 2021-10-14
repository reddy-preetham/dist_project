from crypto_utils import *
# from replica import Replica
class TimeoutInfo:
    def __init__(self,round,high_qc,name="") -> None:
        self.round=round
        self.high_qc=high_qc
        self.sender=name
        self.signature=sign(""+self.round+self.high_qc.round)
class TC:
    def __init__(self,round,tmo_high_qc_rounds,tmo_signatures) -> None:
        self.round=round
        self.tmo_high_qc_rounds=tmo_high_qc_rounds
        self.tmo_signatures=tmo_signatures
class TimeoutMsg:
    def __init__(self,tmo_info,last_round_tc,high_commit_tc) -> None:
        self.tmo_info=tmo_info
        self.last_round_tc=last_round_tc
        self.high_commit_qc=high_commit_tc
class ProposalMsg:
    def __init__(self,block,last_round_tc,high_commit_qc):
        self.block=block
        self.last_round_tc=last_round_tc
        self.high_commit_qc=high_commit_qc
        self.signature=sign(self.block.id)