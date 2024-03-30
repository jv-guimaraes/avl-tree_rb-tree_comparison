from avl_tree import AVLTree
from redblack_tree import RBTree
from abstract_tree import AbstractTree
from random import shuffle, randint

def test_tree(tree: AbstractTree, n: int, name: str):
    nums = [n for n in range(n)]
    
    shuffle(nums)
    for n in nums: tree.insert(n)
    for n in nums: assert(tree.contains(n))

    shuffle(nums)
    for n in nums: tree.delete(n)
    assert(tree.is_empty())

    for _ in range(n): tree.insert(randint(0, n // 2))
    print(f"Finished testing {name}!")
    

test_tree(AVLTree(), 50_000, "AVL Tree")
test_tree(RBTree(), 50_000, "Red-Black tree")