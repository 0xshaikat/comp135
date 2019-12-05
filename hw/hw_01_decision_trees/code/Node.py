'''
@author: Shaikat Islam
@title: hw01_01
@professor: Martin Allen
@date: 25-09-2019
'''
'''
Node: a class describing a binary search tree; optimized to describe a feature
and its index
'''
class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
        self.feature_index = None
        self.feature_name = None

    '''
    is_leaf: returns True if Node is a leaf; False otherwise
    inputs: None
    output: True or False
    '''
    def is_leaf(self):
        if (self.left == None and self.right == None):
            return True
        else:
            return False

    '''
    str() representation of a binary search tree.
    '''
    def __str__(self, depth=0):
        ret = ""
        ret += "\n" + ("\t"*depth) +  str(self.data)
        if self.right != None:
            ret += self.right.__str__(depth + 1)
        if self.left != None:
            ret += self.left.__str__(depth + 1)
        return ret
