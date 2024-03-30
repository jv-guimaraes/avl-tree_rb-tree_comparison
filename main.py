from avl_tree import AVLTree
from redblack_tree import RBTree
from abstract_tree import AbstractTree
from random import randint
from time import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
    insertions = [1_000, 5_000, 10_000, 17_500, 25_000]

    print("Calculando tempos")
    avl_insertions: list[float] = [time_insertions(AVLTree(), i, 5) for i in insertions]
    avl_deletions: list[float] = [time_deletions(AVLTree(), i, 5) for i in insertions]
    rb_insertions: list[float] = [time_insertions(RBTree(), i, 5) for i in insertions]
    rb_deletions: list[float] = [time_deletions(RBTree(), i, 5) for i in insertions]
    print("Tempos calculados com sucesso")
    
    plt.plot(insertions, avl_insertions, label='AVL inserções')
    plt.plot(insertions, avl_deletions, label='AVL remoções')
    plt.plot(insertions, rb_insertions, label='Red-Black inserções')
    plt.plot(insertions, rb_deletions, label='Red-Black remoções')

    plt.xlabel('Número de inserções/remoções')
    plt.ylabel('Tempo (ms)')
    plt.title('Tempo de inserção e remoção de elementos em árvores AVL e Red-Black')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    plt.show()

def time_insertions(tree: AbstractTree, num_insertions: int, num_tests: int):
    test_results: list[float] = []
    for _ in range(num_tests):
        random_numbers = [randint(0, num_insertions) for _ in range(num_insertions)]
        tree.reset()
        start = time()
        for i in range(num_insertions):
            tree.insert(random_numbers[i])
        test_results.append(time() - start)

    average = sum(test_results) / num_tests
    return average * 1000

def time_deletions(tree: AbstractTree, num_deletions: int, num_tests: int):
    test_results: list[float] = []
    for _ in range(num_tests):
        random_numbers = [randint(0, num_deletions) for _ in range(num_deletions)]
        tree.reset()
        for i in range(num_deletions):
            tree.insert(random_numbers[i])
        start = time()
        for i in range(num_deletions):
            tree.delete(random_numbers[i])
        test_results.append(time() - start)

    average = sum(test_results) / num_tests
    return average * 1000

if __name__ == "__main__":
    main()
