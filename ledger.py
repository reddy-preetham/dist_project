from utils import *
import os
from block import Tree
from cacheout import Cache


class LedgerBlock:
    """Ledger block saved in pending ledger state tree
    Consists of state id and payload of transactions.
    """
    def __init__(self, state_id, payload):
        self.id = state_id
        self.payload = payload


class Ledger:
    """Ledger class and functions analogous to pseudocode"""
    # Genesis ledger block which is added to pending ledger tree when created
    genesis_block = LedgerBlock("genesis_state_id", ["genesis transaction"])
    pending_ledger_tree = Tree(genesis_block)
    # block state map to store mappings from block id to state id
    block_state_map = {}

    @classmethod
    def initialize_ledger(cls):
        """Initialize ledger state invoked from Replica"""
        # Cache of commited blocks to return block with block id if commited
        # Cache is set with max size as described in phase 2 document
        cls.commited_blocks = Cache(maxsize = max(Config.window_size, 2*Config.n_replicas))
        cls.ledger_name = "ledgers/"+str(Config.replica_id)+"_ledger"
        cls.block_state_map["genesis_id"] = "genesis_state_id"


    @classmethod
    def speculate(cls,prev_block_id,block):
        """Speculates"""
        parent_state_id=cls.block_state_map.get(prev_block_id,"genesis_state_id")
        state_id=hash((parent_state_id,block.payload))
        
        blk = LedgerBlock(state_id,block.payload)
        cls.pending_ledger_tree.add(blk,parent_state_id)
        
        cls.block_state_map[block.id]=state_id
        
    @classmethod
    def pending_state(cls,block_id): 
        return cls.block_state_map.get(block_id,None)
    @classmethod
    def commit(cls,block):
        # block=cls.pending_ledger_tree.get_block(cls.block_state_map[block_id])
        if block.id not in cls.commited_blocks:
            # print(block.round,block.payload)
            cls.persist(cls.block_state_map[block.id])
            cls.pending_ledger_tree.prune(cls.block_state_map[block.id])
            cls.commited_blocks.set(block.id,block)
    @classmethod
    def committed_block(cls,block_id):
        cls.commited_blocks.get(block_id,None)
    @classmethod
    def persist(cls,state_id):
        with open(cls.ledger_name+".txt", "a") as myfile:
            myfile.write("\n".join(cls.pending_ledger_tree.get_block(state_id).payload)+"\n")
            myfile.flush()
            os.fsync(myfile.fileno())
            
        
