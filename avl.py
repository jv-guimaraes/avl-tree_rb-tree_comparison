from typing import Optional, Any
from io import StringIO
from dataclasses import dataclass
from arvore_abstrata import ArvoreAbstrata

@dataclass
class Nó:
    valor: int
    esquerda: Optional['Nó'] = None
    direita: Optional['Nó'] = None
    altura: int = 1        
         
class ArvoreAVL(ArvoreAbstrata):
    def __init__(self):
        self.raiz = None
        
    def inserir(self, valor: int):
        def _inserir(raiz: Optional[Nó], valor: int) -> Optional[Nó]:
            if not raiz:
                return Nó(valor)
            if valor < raiz.valor:
                raiz.esquerda = _inserir(raiz.esquerda, valor)
            else:
                raiz.direita = _inserir(raiz.direita, valor)

            raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))
            
            return self._balanciar(raiz)
        
        self.raiz = _inserir(self.raiz, valor)
    
    def _buscar_nó(self, valor: int) -> Optional[int]:
        
        def _buscar(raiz: Optional[Nó], valor: int) -> Optional[Nó]:
            if not raiz or raiz.valor == valor:
                return raiz
            
            if valor < raiz.valor:
                return _buscar(raiz.esquerda, valor)
            else:
                return _buscar(raiz.direita, valor)
        
        res = _buscar(self.raiz, valor)
        return res.valor if res else None

    def contem(self, valor: int) -> bool:
        return self._buscar_nó(valor) is not None
        
    def remover(self, valor: int):

        def _remover(raiz: Optional[Nó], value: int) -> Optional[Nó]:
            if not raiz:
                return None

            if value < raiz.valor:
                raiz.esquerda = _remover(raiz.esquerda, value)
            elif value > raiz.valor:
                raiz.direita = _remover(raiz.direita, value)
            else: #Encontrou o valor a ser deletado
                if not raiz.esquerda:  
                    return raiz.direita
                elif not raiz.direita: 
                    return raiz.esquerda
                else: 
                    successor = raiz.direita
                    while successor.esquerda:
                        successor = successor.esquerda
                    raiz.valor = successor.valor
                    raiz.direita = _remover(raiz.direita, successor.valor)

            raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))

            return self._balanciar(raiz)

        self.raiz = _remover(self.raiz, valor)

    
    def esta_vazia(self) -> bool:
        return self.raiz is None

    def resetar(self) -> None:
        self.raiz = None

    def _altura(self, nó: Optional[Nó]) -> int:
        if not nó: return 0
        return nó.altura
    
    def _get_bf(self, nó: Optional[Nó]) -> int:
        if not nó: return 0
        return self._altura(nó.esquerda) - self._altura(nó.direita)

    def _rotar_direita(self, y: Nó) -> Nó:
        assert y.esquerda
        x = y.esquerda
        z = x.direita

        x.direita = y
        y.esquerda = z

        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))

        return x

    def _rotar_esquerda(self, x: Nó) -> Nó:
        assert x.direita
        y = x.direita
        z = y.esquerda

        y.esquerda = x
        x.direita = z

        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))

        return y
   
    def _balanciar(self, raiz: Nó) -> Nó:
        bf = self._get_bf(raiz)
        if bf > 1: # Ta pendendo para a esquerda
            assert raiz.esquerda
            if self._get_bf(raiz.esquerda) >= 0:
                return self._rotar_direita(raiz)
            else:
                raiz.esquerda = self._rotar_esquerda(raiz.esquerda)
                return self._rotar_direita(raiz)
        elif bf < -1:
            assert raiz.direita
            if self._get_bf(raiz.direita) <= 0:
                return self._rotar_esquerda(raiz)
            else:
                raiz.direita = self._rotar_direita(raiz.direita)
                return self._rotar_esquerda(raiz)

        return raiz

    def graph(self, block_size: int = 2) -> str:
        HEIGHT_FACTOR = 2
        def _walk(nó: Optional[Nó], height: int, x: int, y: int, matrix: list[list[Any]]):
            if nó:
                matrix[y][x] = nó
                walk = 2 ** (height - 2)
                _walk(nó.esquerda, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
                _walk(nó.direita, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
        
        h = self._altura(self.raiz)
        w = 2 ** h - 1
        matrix: list[list[Any]] = [[None for _ in range(w)] for _ in range(h * HEIGHT_FACTOR)]
        _walk(self.raiz, h, 2 ** (h - 1) - 1, 0, matrix)
        
        buffer = StringIO()
        for row in matrix:
            for nó in row:
                if nó is None:
                    buffer.write((' ' * block_size) + ' '); continue
                else:
                    buffer.write(f'{nó.value} ')
            buffer.write('\n')
        
        return buffer.getvalue()
