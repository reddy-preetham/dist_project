from utils import *
import utils
import os
from block import Tree
from cacheout import Cache
# from crypto_utils import *

class LedgerBlock:
    def __init__(self,state_id,payload):
        self.id = state_id
        self.payload=payload

class Ledger:    

    genesis_block=LedgerBlock("genesis",["genesis transaction"])
    commited_blocks=Cache(maxsize=max(Config.window_size,2*Config.n_replicas)) 
    pending_ledger_tree = Tree(genesis_block)
    state_block_map={}
    ledger_name = Config.replica_id+"_ledger"

    @classmethod
    def speculate(cls,prev_block_id="genesis",block=genesis_block):
        
        parent_state_id=cls.state_block_map.get(prev_block_id,"genesis")
        state_id=hash((parent_state_id,block.payload))
        
        blk = LedgerBlock(state_id,block.payload)
        cls.pending_ledger_tree.add(blk,parent_state_id)
        cls.state_block_map[block.id]=state_id
        
    @classmethod
    def pending_state(cls,block_id): 
        return cls.state_block_map.get(block_id,None)
    @classmethod
    def commit(cls,block):
        # block=cls.pending_ledger_tree.get_block(cls.state_block_map[block_id])
        cls.persist(cls.state_block_map[block.id])
        cls.pending_ledger_tree.prune(cls.state_block_map[block.id])
        cls.commited_blocks.set(block.id,block)
    @classmethod
    def committed_block(cls,block_id):
        cls.commited_blocks.get(block_id,None)
    @classmethod
    def persist(cls,state_id):
        with open(cls.ledger_name+".txt", "a") as myfile:
            myfile.write("\n".join(cls.pending_ledger_tree.get_block(state_id).payload))
            myfile.flush()
            os.fsync(myfile.fileno())
            
        
