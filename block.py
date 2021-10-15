# from block_tree import Block
# from crypto_utils import genesis_block
class Node:
    def __init__(self, blk):
        self.blk = blk
        self.children = list()

    def get_children(self):
        return self.children

class Tree:
    def __init__(self,blk):
        self.root = Node(blk)
        self.map = {}
        self.map.setdefault(self.root.blk.id,self.root)
        self.map[self.root.blk.id] = self.root

    def pruning(self, blk_id):
        self.root = self.map.get(blk_id)
        #need to remove pruned elements from map


    def add(self, blk, parent_id=None):
        node = Node(blk)
        self.map[blk.id] = node
        if parent_id:
            self.map[parent_id].get_children().append(node)
        else:
            parent_id = blk.qc.vote_info.id
            self.map[parent_id].get_children().append(node)
    
    def get_block(self,block_id):
        return self.map[block_id].blk
        