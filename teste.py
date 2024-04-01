from avl import ArvoreAVL
from redblack import ArvoreRedBlack
from arvore_abstrata import ArvoreAbstrata
from random import shuffle, randint

def testar_arvore(tree: ArvoreAbstrata, n: int, name: str):
    nums = [n for n in range(n)]
    
    shuffle(nums)
    for n in nums: tree.inserir(n)
    for n in nums: assert(tree.contem(n))

    shuffle(nums)
    for n in nums: tree.remover(n)
    assert(tree.esta_vazia())

    for _ in range(n): tree.inserir(randint(0, n // 2))
    print(f"Terminou de testar: {name}!")
    

testar_arvore(ArvoreAVL(), 20_000, "AVL")
testar_arvore(ArvoreRedBlack(), 20_000, "Red-Black")