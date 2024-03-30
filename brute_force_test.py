from avl_tree import AVLTree
from redblack_tree import RBTree
from random import shuffle, randint

def test_tree(tree_type: type, n: int):
    tree = tree_type()
    nums = [n for n in range(n)]
    
    shuffle(nums)
    for n in nums: tree.insert(n)
    for n in nums: assert(tree.contains(n))

    shuffle(nums)
    for n in nums: tree.delete(n)
    assert(tree.is_empty())

    tree = tree_type()
    for _ in range(n): tree.insert(randint(0, n // 2))
    print(f"Finished testing {tree_type.__name__}!")
    

test_tree(AVLTree, 50_000)
test_tree(RBTree, 50_000)