from replica import *
from cacheout import Cache
import os
from block import Tree

class Ledger:    

    def __init__(self) -> None:
        self.commited_blocks=Cache(maxsize=max(window_size,2*num_validators)) 
        self.pending_ledger_tree = Tree(block = ["Genesis transactions!!"])
        self.state_block_map={}
        self.ledger_name = Replica.getName()+"_ledger"
        pass

    def speculate(self,prev_block_id,block):
        parent_state_id=self.state_block_map(prev_block_id)
        state_id = self.pending_ledger_tree.add(parent_state_id,block.payload)
        self.state_block_map[block.id]=state_id

    def pending_state(self,block_id): 
        return self.state_block_map[block_id]

    def commit(self,block_id):
        block=self.pending_ledger_tree.get_block(self.state_block_map[block_id])
        self.persist(self.state_block_map[block_id])
        self.pending_ledger_tree.prune(self.state_block_map[block_id])
        self.commited_blocks.set(block_id,block)

    def commited_block(self,block_id):
        self.commited_blocks.get(block_id,default=None)

    def persist(self,state_id):
        with open(self.ledger_name+".txt", "a") as myfile:
            myfile.write("\n".join(self.pending_ledger_tree.get_block(state_id)))
            myfile.flush()
            os.fsync(myfile.fileno)
            
        
