from ledger import Ledger
from vote_info import VoteInfo
from block_tree import LedgerCommitInfo, BlockTree,VoteMsg
from timeout import TimeoutInfo
from crypto_utils import *
class Safety:

    def __init__(self) -> None:
        self.__private_key
        self.__public_keys
        self.__highest_vote_round=0
        self.__highest_qc_round

    def set_keys(self,private_key,public_keys):
        self.__private_key=private_key
        self.__public_key=public_keys

    def __increase_highest_vote_round(self,round):
        self.__highest_vote_round=max(round,self.__highest_vote_round)
    def __update_highest_qc_round(self,qc_round):
        self.__highest_qc_round=max(qc_round,self.__highest_qc_round)
    def __consecutive(block_round,round):
        return round+1==block_round
    def __safe_to_extend(self,block_round,qc_round,tc):
        return self.__consecutive(block_round,tc.round) and qc_round>=max(tc.tmo_high_qc_rounds)
    def __safe_to_vote(self,block_round,qc_round,tc):
        if block_round<=max(self.__highest_vote_round,qc_round):
            return False
        return self.__consecutive(block_round,qc_round) or self.__safe_to_extend(block_round,qc_round,tc)
    def __safe_to_timeout(self,round,qc_round,tc):
        if qc_round<self.__highest_qc_round or round<=max(self.__highest_vote_round-1,qc_round):
            return False
        return self.__consecutive(round,qc_round) or self.__consecutive(round,tc.round)
    def __commit_state_id_candidate(self,block_round,qc):
        if self.__consecutive(block_round,qc.vote_info_round):
            return Ledger.pending_state(qc.id)
        else:
            return None

    def __valid_signatures(sig_list):
        return True
    
    def make_vote(self,b,last_tc):
        qc_round=b.qc.vote_info.round
        if self.__valid_signatures((b,last_tc)) and self.__safe_to_vote(b.round,qc_round,last_tc):
            self.__update_highest_qc_round(qc_round)
            self.__increase_highest_vote_round(b.round)
            vote_info=VoteInfo(id=b.id,round=b.round,parent_id=b.qc.vote_info.id,parentround=qc_round,exec_state_id=Ledger.pending_state(b.id))
            ledger_commit_info=LedgerCommitInfo(commit_state_id=self.__commit_state_id_candidate(b.round,b.qc),vote_info_hash=hash(vote_info))
            return VoteMsg(vote_info,ledger_commit_info,BlockTree.high_commit_qc)
        return None
    def make_timeout(self,round,high_qc,last_tc):
        qc_round=high_qc.vote_info.round
        if self.__valid_signatures((high_qc,last_tc)) and self.__safe_to_timeout(round,qc_round,last_tc):
            self.__increase_highest_vote_round(round)
            return TimeoutInfo(round,high_qc)
        return None

