from avl import AVLTree
from random import randint
import os

if __name__ == "__main__":
    tree = AVLTree()

    while True:
        command = input().split(' ')
        match command[0]:
            case 'i':
                tree.insert(int(command[1]))
                os.system('cls')
                print(tree.graph())
            case 'd':
                tree.delete(int(command[1]))
                os.system('cls')
                print(tree.graph())
            case 's':
                print("Found:", tree.search(int(command[1])))
            case 'r':
                num = randint(10, 99)
                tree.insert(num)
                os.system('cls')
                print(tree.graph())
                print(f'Tried to insert {num}')
            case 'p':
                tree.inorder()
            case 't':
                for i in range(100_000):
                    tree.insert(randint(0, 75_000))
                print("Insertion test finished.")
                for i in range(100_000):
                    tree.delete(randint(0, 75_000))
                print("Deletion test finished.")
                tree = AVLTree()
            case 't2':
                numbers = [randint(0, 50_000) for _ in range(50_000)]
                for num in numbers:
                    tree.insert(num)
                for num in numbers:
                    tree.delete(num)
                tree.inorder()
                print("finished")
                tree = AVLTree()
            case _:
                break

