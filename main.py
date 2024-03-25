import os
import random
from avl import AVLTree

BLOCK_SIZE = 1
SHOW_PARENT = False
tree = AVLTree()

while True:
    try:
        command = input("Insert a command: ")
        command = command.split(' ')
        if len(command) >= 2:
            (command, num) = command[0], int(command[1])
        else:
            (command, num) = command[0], 0

    except:
        break
    
    match command:
        case 'i':
            tree.insert(int(num))
            os.system('cls'); print(tree.graph(BLOCK_SIZE, SHOW_PARENT))
        case 's':
            print(f'Found: {tree.search(int(num))}\n')
        case 'r':
            randnum = random.randint(10, 99)
            tree.insert(randnum)
            os.system('cls'); print(tree.graph(BLOCK_SIZE, SHOW_PARENT))
            print(f'Tried to insert {randnum}')
        case 'rr':
            tree.rotate(num, 'right')
            os.system('cls'); print(tree.graph(BLOCK_SIZE, SHOW_PARENT))
        case 'rl':
            tree.rotate(num, 'left')
            os.system('cls'); print(tree.graph(BLOCK_SIZE, SHOW_PARENT))   
        case 'q':
            break
        case _:
            print("Fucky command inserted.")

    
