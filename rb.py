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
        new_node = Node(value)
        # if new_node.value == 25: new_node.color = Color.BLACK
        
        if self.root is None:
            self.root = new_node
        else:
            self._insert(new_node)

        self._fix_insert(new_node)
    
    def _insert(self, new_node: Node):
        assert(self.root)
        curr_node = self.root
        value = new_node.value

        while True:
            if value <= curr_node.value:
                if curr_node.left is None:
                    curr_node.left = new_node
                    break
                curr_node = curr_node.left
            else:
                if curr_node.right is None:
                    curr_node.right = new_node
                    break
                curr_node = curr_node.right
        
        new_node.parent = curr_node


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

    def rotate_right(self, node: Node):
        assert node.left
        parent = node.parent
        child = node.left
        node.left = child.right
        if child.right:
            child.right.parent = node
        
        child.right = node
        node.parent = child
        child.parent = parent
        
        if parent:
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child
        else:
            self.root = child

    def rotate_left(self, node: Node):
        assert node.right
        parent = node.parent
        child = node.right
        node.right = child.left
        if child.left:
            child.left.parent = node
        
        child.left = node
        node.parent = child
        child.parent = parent
        
        if parent:
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child
        else:
            self.root = child

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
