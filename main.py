from avl import AVLTree
from os import system

if __name__ == "__main__":
    tree = AVLTree()

    while True:
        try:
            num = int(input('Inserir: '))
        except:
            break
        tree.insert_key(num)
        system('cls')
        print(tree.graph())