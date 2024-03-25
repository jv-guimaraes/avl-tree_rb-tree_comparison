from avl import AVLTree
from random import randint

def test_avl_tree():
    tree = AVLTree()
    conjunto: set[int] = set()
    n = 50_000

    for _ in range(n):
        num = randint(0, n)
        tree.insert(num)
        conjunto.add(num)
        assert(num in conjunto and tree.search(num) == num)

    for _ in range(n):
        num = randint(0, n)
        tree.delete(num)
        try: conjunto.remove(num)
        except: pass
        assert(num not in conjunto and tree.search(num) is None)
    
    print("Finished testing!")

test_avl_tree()