from avl import AVLTree
from rb import RBTree
from random import randint

def test_avl_tree():
    tree = AVLTree()
    conjunto: set[int] = set()
    n = 10_000

    for _ in range(n):
        num = randint(0, n)
        tree.insert(num)
        conjunto.add(num)
        assert(num in conjunto and tree.contains(num))

    for _ in range(n):
        num = randint(0, n)
        tree.delete(num)
        try: conjunto.remove(num)
        except: pass
        assert(num not in conjunto and not tree.contains(num))
    
    print("Finished testing AVL Tree!")

def test_rb_tree():
    tree = RBTree()
    conjunto: set[int] = set()
    n = 10_000

    for _ in range(n):
        num = randint(0, n)
        tree.insert(num)
        conjunto.add(num)
        assert(num in conjunto and tree.contains(num))

    for _ in range(n):
        num = randint(0, n)
        tree.delete(num)
        try: conjunto.remove(num)
        except: pass
        assert(num not in conjunto and not tree.contains(num))
    
    print("Finished testing Red-Black tree!")

test_avl_tree()
test_rb_tree()