from avl import ArvoreAVL
from redblack import ArvoreRedBlack
from arvore_abstrata import ArvoreAbstrata
from random import randint
from time import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
    inserções = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]
    # inserções = [1_000, 10_000, 25_000]

    print("Calculando tempos")
    avl_inserções: list[float] = [medir_inserções_ms(ArvoreAVL(), i, 3) for i in inserções]
    avl_remoções: list[float] = [medir_remoções_ms(ArvoreAVL(), i, 3) for i in inserções]
    rb_inserções: list[float] = [medir_inserções_ms(ArvoreRedBlack(), i, 3) for i in inserções]
    rb_remoções: list[float] = [medir_remoções_ms(ArvoreRedBlack(), i, 3) for i in inserções]
    print("Tempos calculados com sucesso")
    
    plt.plot(inserções, avl_inserções, label='AVL inserções', marker='o')
    plt.plot(inserções, avl_remoções, label='AVL remoções', marker='o')
    plt.plot(inserções, rb_inserções, label='Red-Black inserções', marker='o')
    plt.plot(inserções, rb_remoções, label='Red-Black remoções', marker='o')

    plt.xlabel('Número de inserções/remoções')
    plt.ylabel('Tempo (ms)')
    plt.title('Tempo de inserção e remoção de elementos em árvores AVL e Red-Black')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    plt.show()

def medir_inserções_ms(arvore: ArvoreAbstrata, num_inserções: int, num_testes: int):
    resultados: list[float] = []
    for _ in range(num_testes):
        random_numbers = [randint(0, num_inserções) for _ in range(num_inserções)]
        arvore.resetar()
        start = time()
        for i in range(num_inserções):
            arvore.inserir(random_numbers[i])
        resultados.append(time() - start)

    media = sum(resultados) / num_testes
    return media * 1000

def medir_remoções_ms(arvore: ArvoreAbstrata, num_remoções: int, num_testes: int):
    resultados: list[float] = []
    for _ in range(num_testes):
        random_numbers = [randint(0, num_remoções) for _ in range(num_remoções)]
        arvore.resetar()
        for i in range(num_remoções):
            arvore.inserir(random_numbers[i])
        start = time()
        for i in range(num_remoções):
            arvore.remover(random_numbers[i])
        resultados.append(time() - start)

    media = sum(resultados) / num_testes
    return media * 1000

if __name__ == "__main__":
    main()
