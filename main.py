import os
from avl import AVLTree

tree = AVLTree()
while True:
    try:
        command = input("Insert a command: ")
        command = command.split(' ')
        (command, num) = command[0], int(command[1])
    except:
        break
    
    match command:
        case 'i':
            tree.insert(num)
            os.system('cls')
            print(tree.graph())
        case 's':
            print(f'Found: {tree.search(num)}\n')
        case _:
            print("Incorrect command.\n")

    
