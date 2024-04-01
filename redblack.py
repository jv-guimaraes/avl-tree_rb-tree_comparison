from io import StringIO
from typing import Any
from arvore_abstrata import ArvoreAbstrata

PRETO = 0
VERMELHO = 1

class Nó:
    valor: int
    esquerda: 'Nó'
    direita: 'Nó' 
    pai: 'Nó' 
    cor: int

    def __init__(self, valor: int, cor: int = VERMELHO) -> None:
        self.valor = valor
        self.cor = cor

class ArvoreRedBlack(ArvoreAbstrata):
    raiz: Nó
    nulo = Nó(valor=-1, cor=PRETO)

    def __init__(self) -> None:
        self.raiz = self.nulo

    def inserir(self, valor: int) -> None:
        z = Nó(valor)
        y = self.nulo
        x = self.raiz
        while x  != self.nulo:
            y = x
            if z.valor < x.valor:
                x = x.esquerda
            else:
                x = x.direita
        z.pai = y
        if y == self.nulo:
            self.raiz = z
        elif z.valor < y.valor:
            y.esquerda = z
        else:
            y.direita = z
        z.esquerda = self.nulo
        z.direita = self.nulo
        self._fix_inserir(z)

    def _fix_inserir(self, z: Nó):
        while z.pai.cor == VERMELHO:
            p_e = (z.pai == z.pai.pai.esquerda) # Se o pai é filho esquerdo
            y = z.pai.pai.direita if p_e else z.pai.pai.esquerda
            if y.cor == VERMELHO:
                z.pai.cor = PRETO
                y.cor = PRETO
                z.pai.pai.cor = VERMELHO
                z = z.pai.pai
            else:
                if z == (z.pai.direita if p_e else z.pai.esquerda):
                    z = z.pai
                    self._rotar_esquerda(z) if p_e else self._rotar_direita(z)                        
                z.pai.cor = PRETO
                z.pai.pai.cor = VERMELHO
                self._rotar_direita(z.pai.pai) if p_e else self._rotar_esquerda(z.pai.pai)
        self.raiz.cor = PRETO

    def _transplantar(self, u: Nó, v: Nó):
        if u.pai == self.nulo:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def _minimo(self, raiz: Nó) -> Nó:
        while raiz.esquerda != self.nulo:
            raiz = raiz.esquerda
        return raiz
            
    def remover(self, valor: int):
        z = self._buscar_nó(valor)
        if z == self.nulo: return
        y = z
        y_original_color = y.cor
        if z.esquerda == self.nulo:
            x = z.direita
            self._transplantar(z, z.direita)
        elif z.direita == self.nulo:
            x = z.esquerda
            self._transplantar(z, z.esquerda)
        else:
            y = self._minimo(z.direita)
            y_original_color = y.cor
            x = y.direita
            if y != z.direita:
                self._transplantar(y, y.direita)
                y.direita = z.direita
                y.direita.pai = y
            else:
                x.pai = y
            self._transplantar(z, y)
            y.esquerda = z.esquerda
            y.esquerda.pai = y
            y.cor = z.cor
        if y_original_color == PRETO:
            self._fix_remover(x)

    def _fix_remover(self, x: Nó):
        while x != self.raiz and x.cor == PRETO:
            if x == x.pai.esquerda:
                w = x.pai.direita
                if w.cor == VERMELHO:
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotar_esquerda(x.pai)
                    w = x.pai.direita
                if w.esquerda.cor == PRETO and w.direita.cor == PRETO:
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.direita.cor == PRETO:
                        w.esquerda.cor = PRETO
                        w.cor = VERMELHO
                        self._rotar_direita(w)
                        w = x.pai.direita
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.direita.cor = PRETO
                    self._rotar_esquerda(x.pai)
                    x = self.raiz
            else:
                w = x.pai.esquerda
                if w.cor == VERMELHO:
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotar_direita(x.pai)
                    w = x.pai.esquerda
                if w.direita.cor == PRETO and w.esquerda.cor == PRETO:
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.esquerda.cor == PRETO:
                        w.direita.cor = PRETO
                        w.cor = VERMELHO
                        self._rotar_esquerda(w)
                        w = x.pai.esquerda
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.esquerda.cor = PRETO
                    self._rotar_direita(x.pai)
                    x = self.raiz
        x.cor = PRETO

    def contem(self, valor: int) -> bool:
        return self._buscar_nó(valor) != self.nulo
    
    def _buscar_nó(self, valor: int) -> Nó:
        def _search(nó: Nó, valor: int) -> Nó:
            if nó == self.nulo: return self.nulo
            if valor == nó.valor: return nó
            if valor <= nó.valor: return _search(nó.esquerda, valor)
            return _search(nó.direita, valor)
        return _search(self.raiz, valor)

    def _rotar_direita(self, x: Nó):
        y = x.esquerda
        x.esquerda = y.direita
        if y.direita != self.nulo:
            y.direita.pai = x
        y.pai = x.pai
        if x.pai == self.nulo:
            self.raiz = y
        elif x == x.pai.direita:
            x.pai.direita = y
        else:
            x.pai.esquerda = y
        y.direita = x
        x.pai = y
    
    def _rotar_esquerda(self, x: Nó):
        y = x.direita
        x.direita = y.esquerda
        if y.esquerda != self.nulo:
            y.esquerda.pai = x
        y.pai = x.pai
        if x.pai == self.nulo:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
        y.esquerda = x
        x.pai = y

    def esta_vazia(self) -> bool:
        return self.raiz == self.nulo
    
    def resetar(self) -> None:
        self.raiz = self.nulo

    def graph(self, block_size: int = 2) -> str:
        def _height(raiz: Nó) -> int:
            if raiz == self.nulo:
                return 0
            return 1 + max(_height(raiz.esquerda), _height(raiz.direita))  
        
        def _walk(nó: Nó, height: int, x: int, y: int, matrix: list[list[Any]]):
            if nó != self.nulo:
                matrix[y][x] = nó
                walk = 2 ** (height - 2)
                _walk(nó.esquerda, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
                _walk(nó.direita, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
        
        HEIGHT_FACTOR = 2
        h = _height(self.raiz)
        w = 2 ** h - 1
        matrix: list[list[Any]] = [[self.nulo for _ in range(w)] for _ in range(h * HEIGHT_FACTOR)]
        _walk(self.raiz, h, 2 ** (h - 1) - 1, 0, matrix)
        
        buffer = StringIO()
        for row in matrix:
            for nó in row:
                if nó == self.nulo:
                    buffer.write((' ' * block_size) + ' '); continue
                else:            
                    if nó.cor == PRETO:
                        buffer.write(f'{nó.valor}B ')
                    else:
                        buffer.write(f'{nó.valor}R ')

            buffer.write('\n')
        
        return buffer.getvalue()
