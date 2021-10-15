from ledger import Ledger
from block_tree import VoteInfo
from block_tree import LedgerCommitInfo, BlockTree,VoteMsg
from timeout import TimeoutInfo
from utils import *
class Safety:

    __private_key=Config.private_key
    __public_keys=Config.replica_pub_keys
    __highest_vote_round=0
    __highest_qc_round=-1

    # @classmethod
    # def set_keys(cls,private_key,public_keys):
    #     self.__private_key=private_key
    #     self.__public_key=public_keys

    @classmethod
    def __increase_highest_vote_round(cls,round):
        cls.__highest_vote_round=max(round,cls.__highest_vote_round)
    @classmethod
    def __update_highest_qc_round(cls,qc_round):
        cls.__highest_qc_round=max(qc_round,cls.__highest_qc_round)
    @classmethod
    def __consecutive(cls,block_round,round):
        return round+1==block_round
    @classmethod
    def __safe_to_extend(cls,block_round,qc_round,tc):
        return cls.__consecutive(block_round,tc.round) and qc_round>=max(tc.tmo_high_qc_rounds)
    @classmethod
    def __safe_to_vote(cls,block_round,qc_round,tc):
        if block_round<=max(cls.__highest_vote_round,qc_round):
            return False
        return cls.__consecutive(block_round,qc_round) or cls.__safe_to_extend(block_round,qc_round,tc)
    @classmethod
    def __safe_to_timeout(cls,round,qc_round,tc):
        if qc_round<cls.__highest_qc_round or round<=max(cls.__highest_vote_round-1,qc_round):
            return False
        return cls.__consecutive(round,qc_round) or cls.__consecutive(round,tc.round)
    @classmethod
    def __commit_state_id_candidate(cls,block_round,qc):
        if cls.__consecutive(block_round,qc.vote_info.round):
            return Ledger.pending_state(qc.vote_info.id)
        else:
            return None
    @classmethod
    def __valid_signatures(cls,sig_list):
        return True
    @classmethod
    def make_vote(cls,b,last_tc):
        qc_round=b.qc.vote_info.round
        if cls.__valid_signatures((b,last_tc)) and cls.__safe_to_vote(b.round,qc_round,last_tc):
            cls.__update_highest_qc_round(qc_round)
            cls.__increase_highest_vote_round(b.round)
            vote_info=VoteInfo(id=b.id,round=b.round,parent_id=b.qc.vote_info.id,parent_round=qc_round,exec_state_id=Ledger.pending_state(b.id))
            ledger_commit_info=LedgerCommitInfo(commit_state_id=cls.__commit_state_id_candidate(b.round,b.qc),vote_info_hash=hash(vote_info))
            return VoteMsg(vote_info,ledger_commit_info,BlockTree.high_commit_qc)
        return None
    @classmethod
    def make_timeout(cls,round,high_qc,last_tc):
        qc_round=high_qc.vote_info.round
        if cls.__valid_signatures((high_qc,last_tc)) and cls.__safe_to_timeout(round,qc_round,last_tc):
            cls.__increase_highest_vote_round(round)
            return TimeoutInfo(round,high_qc)
        return None

