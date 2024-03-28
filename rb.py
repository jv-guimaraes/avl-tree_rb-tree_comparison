from dataclasses import dataclass
from io import StringIO
from typing import Optional, Any
from enum import Enum

class Color(Enum):
    BLACK = 0
    RED = 1,

class Side(Enum):
    LEFT = 0,
    RIGHT = 1

@dataclass
class Node:
    value: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    parent: Optional['Node'] = None
    color: Color = Color.RED

    def is_red(self) -> bool:
        return self.color == Color.RED
    
    def is_black(self) -> bool:
        return self.color == Color.BLACK

    def is_root(self) -> bool:
        return self.parent is None
    
    def switch_color(self) -> None:
        self.color = Color.BLACK if self.color == Color.RED else Color.RED

    def side(self) -> Side:
        assert self.parent
        if self.value <= self.parent.value:
            return Side.LEFT
        return Side.RIGHT
    
    def uncle(self) -> Optional['Node']:
        if (not self.parent) or (not self.parent.parent):
            return None
        if self.parent.side() == Side.RIGHT:
            return self.parent.parent.left
        else:
            return self.parent.parent.right

@dataclass
class RBTree:
    root: Optional['Node'] = None

    def __str__(self) -> str:
        if self.root is None:
            return ""
        return graph(self.root)

    def insert(self, value: int) -> None:
        z = Node(value)
        y: Optional[Node] = None
        x = self.root
        while x is not None:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z
        self._fix_insert(z)

    def _fix_insert(self, node: Node):
        # Case 0: Root is red
        if node.parent is None:
            node.switch_color()
            return

        if not (node.is_red() and node.parent.is_red()):
            return
        
        # Case 1: Father and uncle are red
        uncle = node.uncle()
        if node.parent.is_red() and uncle and uncle.is_red():
            assert node.parent.parent
            node.parent.switch_color()
            node.parent.parent.switch_color()
            uncle.switch_color()
            self._fix_insert(node.parent.parent)
        
        # Case 2 or 3: Father is red and uncle is black
        if node.parent.is_red() and (uncle is None or uncle.is_black()):
            # Case 2: Triangle
            if node.parent.side() != node.side():
                
                if node.side() == Side.LEFT:
                    self.rotate_right(node.parent)
                    new_node_to_be_fixed = node.right
                else:
                    self.rotate_left(node.parent)
                    new_node_to_be_fixed = node.left
                assert new_node_to_be_fixed
                self._fix_insert(new_node_to_be_fixed)
            else: # Case 3: Line
                # Rotate grandparent to opposite side of node and recolor parent and grandparent
                assert node.parent.parent
                og_parent, og_grandparent = node.parent, node.parent.parent
                if node.side() == Side.LEFT:
                    self.rotate_right(node.parent.parent)
                else:
                    self.rotate_left(node.parent.parent)
                og_parent.switch_color()
                og_grandparent.switch_color()
    
    def contains(self, value: int) -> bool:
        return self.find_node(value) is not None
    
    def find_node(self, value: int) -> Optional[Node]:
        def _search(node: Optional[Node], value: int) -> Optional[Node]:
            if node is None: return None
            if value == node.value: return node
            if value <= node.value: return _search(node.left, value)
            return _search(node.right, value)
        return _search(self.root, value)

    def rotate_right(self, x: Node):
        assert x.left
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    
    def rotate_left(self, x: Node):
        assert x.right
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

def graph(root: Node, block_size: int = 2) -> str:
    def _height(root: Optional[Node]) -> int:
        if root is None:
            return 0
        return 1 + max(_height(root.left), _height(root.right))  
    
    HEIGHT_FACTOR = 2
    def _walk(node: Optional[Node], height: int, x: int, y: int, matrix: list[list[Any]]):
        if node:
            matrix[y][x] = node
            walk = 2 ** (height - 2)
            _walk(node.left, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
            _walk(node.right, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
    
    h = _height(root)
    w = 2 ** h - 1
    matrix: list[list[Any]] = [[None for _ in range(w)] for _ in range(h * HEIGHT_FACTOR)]
    _walk(root, h, 2 ** (h - 1) - 1, 0, matrix)
    
    buffer = StringIO()
    for row in matrix:
        for node in row:
            if node is None:
                buffer.write((' ' * block_size) + ' '); continue
            else:            
                if node.color == Color.BLACK:
                    buffer.write(f'{node.value}B ')
                else:
                    buffer.write(f'{node.value}R ')

        buffer.write('\n')
    
    return buffer.getvalue()
