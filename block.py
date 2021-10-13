from block_tree import Block
class Node:
    def __init__(self, block):
        self.block = block
        self.children = list()
    
    def get_block(self):
        return self.block

    def get_children(self):
        return self.children

class Tree:
    def __init__(self):
        self.root = Node(Block.genesis_block)
        self.map = map()
        self.map[Block.genesis_block.id] = self.root

    def pruning(self, id):
        self.root = map.get(id)
        #need to remove pruned elements from map


    def add(self, block, parent_id=None):
        node = Node(block)
        self.map[block.id] = node
        if parent_id:
            self.map[parent_id].get_children().add(node)
        else:
            parent_id = block.qc.vote_info.id
            self.map[parent_id].get_children().add(node)
    
    def get_block(self,block_id):
        return self.map[block_id].get_block()
        