from io import StringIO
from typing import Any, Optional
from enum import Enum


class Color(Enum):
    BLACK = 0
    RED = 1,

class Side(Enum):
    LEFT = 0,
    RIGHT = 1

class Node:
    value: Any
    left: 'Node'
    right: 'Node' 
    p: 'Node' 
    color: Color = Color.RED

    def __init__(self, value: Any, color: Color = Color.RED) -> None:
        self.value = value

        self.color = color

    def is_red(self) -> bool:
        return self.color == Color.RED
    
    def is_black(self) -> bool:
        return self.color == Color.BLACK
    
    def switch_color(self) -> None:
        self.color = Color.BLACK if self.color == Color.RED else Color.RED

    def side(self) -> Side:
        assert self.p
        if self.value <= self.p.value:
            return Side.LEFT
        return Side.RIGHT


class RBTree:
    root: Node
    nil = Node(value=None, color=Color.BLACK)

    def __init__(self) -> None:
        self.root = self.nil

    def __str__(self) -> str:
        if self.root == self.nil:
            return ""
        return graph(self, self.root)

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
        pass

    def contains(self, value: int) -> bool:
        return self.find_node(value) != self.nil
    
    def find_node(self, value: int) -> Optional[Node]:
        def _search(node: Node, value: int) -> Optional[Node]:
            if node == self.nil: return None
            if value == node.value: return node
            if value <= node.value: return _search(node.left, value)
            return _search(node.right, value)
        return _search(self.root, value)

    def rotate_right(self, x: Node):
        assert x.left
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
    
    def rotate_left(self, x: Node):
        assert x.right
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


def graph(tree: RBTree, root: Node, block_size: int = 2) -> str:
    def _height(root: Node) -> int:
        if root == tree.nil:
            return 0
        return 1 + max(_height(root.left), _height(root.right))  
    
    def _walk(node: Node, height: int, x: int, y: int, matrix: list[list[Any]]):
        if node != tree.nil:
            matrix[y][x] = node
            walk = 2 ** (height - 2)
            _walk(node.left, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
            _walk(node.right, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
    
    HEIGHT_FACTOR = 2
    h = _height(root)
    w = 2 ** h - 1
    matrix: list[list[Any]] = [[tree.nil for _ in range(w)] for _ in range(h * HEIGHT_FACTOR)]
    _walk(root, h, 2 ** (h - 1) - 1, 0, matrix)
    
    buffer = StringIO()
    for row in matrix:
        for node in row:
            if node == tree.nil:
                buffer.write((' ' * block_size) + ' '); continue
            else:            
                if node.color == Color.BLACK:
                    buffer.write(f'{node.value}B ')
                else:
                    buffer.write(f'{node.value}R ')

        buffer.write('\n')
    
    return buffer.getvalue()
