from utils import *


class Node:
    """Node creation for the Tree.
    Contains blk data and all successive blocks nodes in the children list"""
    def __init__(self, blk):
        self.blk = blk
        self.children = list()


class Tree:
    """Tree data structure for storing pending blocks"""
    def __init__(self, blk):
        self.root = Node(blk)
        self.map = {}
        self.map.setdefault(self.root.blk.id, self.root)
        self.map[self.root.blk.id] = self.root

    def prune(self, blk_id):
        """Updated the root node of the tree so that the
        commited blocks won't exist when we traverse the tree from root"""
        self.root = self.map.get(blk_id)

    def add(self, blk, parent_id=None):
        """Adding new block to the tree"""
        node = Node(blk)
        self.map[blk.id] = node
        if parent_id:
            self.map[parent_id].children.append(node)
        else:
            parent_id = blk.qc.vote_info.id
            self.map[parent_id].children.append(node)

    def get_block(self, block_id):
        """Returns block when block id is requested"""
        return self.map[block_id].blk
