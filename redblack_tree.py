from io import StringIO
from typing import Any
from abstract_tree import AbstractTree

BLACK = 0
RED = 1

class Node:
    value: int
    left: 'Node'
    right: 'Node' 
    p: 'Node' 
    color: int

    def __init__(self, value: int, color: int = RED) -> None:
        self.value = value
        self.color = color

class RBTree(AbstractTree):
    root: Node
    nil = Node(value=-1, color=BLACK)

    def __init__(self) -> None:
        self.root = self.nil

    def insert(self, value: int) -> None:
        z = Node(value)
        y = self.nil
        x = self.root
        while x  != self.nil:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y == self.nil:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        self._fix_insert(z)

    def _fix_insert(self, z: Node):
        while z.p.color == RED:
            p_left = (z.p == z.p.p.left) # Se o pai é filho esquerdo
            y = z.p.p.right if p_left else z.p.p.left
            if y.color == RED:
                z.p.color = BLACK
                y.color = BLACK
                z.p.p.color = RED
                z = z.p.p
            else:
                if z == (z.p.right if p_left else z.p.left):
                    z = z.p
                    self._rotate_left(z) if p_left else self._rotate_right(z)                        
                z.p.color = BLACK
                z.p.p.color = RED
                self._rotate_right(z.p.p) if p_left else self._rotate_left(z.p.p)
        self.root.color = BLACK

    def _transplant(self, u: Node, v: Node):
        if u.p == self.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def _minimum(self, root: Node) -> Node:
        while root.left != self.nil:
            root = root.left
        return root
            
    def delete(self, value: int):
        z = self._search_node(value)
        if z == self.nil: return
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y != z.right:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            else:
                x.p = y
            self._transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_original_color == BLACK:
            self._fix_delete(x)

    def _fix_delete(self, x: Node):
        while x != self.root and x.color == BLACK:
            if x == x.p.left:
                w = x.p.right
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self._rotate_left(x.p)
                    w = x.p.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._rotate_right(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.right.color = BLACK
                    self._rotate_left(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self._rotate_right(x.p)
                    w = x.p.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._rotate_left(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.left.color = BLACK
                    self._rotate_right(x.p)
                    x = self.root
        x.color = BLACK

    def contains(self, value: int) -> bool:
        return self._search_node(value) != self.nil
    
    def _search_node(self, value: int) -> Node:
        def _search(node: Node, value: int) -> Node:
            if node == self.nil: return self.nil
            if value == node.value: return node
            if value <= node.value: return _search(node.left, value)
            return _search(node.right, value)
        return _search(self.root, value)

    def _rotate_right(self, x: Node):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y
    
    def _rotate_left(self, x: Node):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def is_empty(self) -> bool:
        return self.root == self.nil
    
    def reset(self) -> None:
        self.root = self.nil

    def graph(self, block_size: int = 2) -> str:
        def _height(root: Node) -> int:
            if root == self.nil:
                return 0
            return 1 + max(_height(root.left), _height(root.right))  
        
        def _walk(node: Node, height: int, x: int, y: int, matrix: list[list[Any]]):
            if node != self.nil:
                matrix[y][x] = node
                walk = 2 ** (height - 2)
                _walk(node.left, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
                _walk(node.right, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
        
        HEIGHT_FACTOR = 2
        h = _height(self.root)
        w = 2 ** h - 1
        matrix: list[list[Any]] = [[self.nil for _ in range(w)] for _ in range(h * HEIGHT_FACTOR)]
        _walk(self.root, h, 2 ** (h - 1) - 1, 0, matrix)
        
        buffer = StringIO()
        for row in matrix:
            for node in row:
                if node == self.nil:
                    buffer.write((' ' * block_size) + ' '); continue
                else:            
                    if node.color == BLACK:
                        buffer.write(f'{node.value}B ')
                    else:
                        buffer.write(f'{node.value}R ')

            buffer.write('\n')
        
        return buffer.getvalue()
