from dataclasses import dataclass
from io import StringIO
import os
from typing import Optional, Any
from enum import Enum

def main():
    tree = RBTree()

    while True:
        command = input().split(' ')
        match command[0]:
            case 'i':
                tree.insert(int(command[1]))
                os.system('cls')
                print(tree)
            case 'rr':
                assert tree.root
                tree.rotate_right(tree.root)
                os.system('cls')
                print(tree)
            case 'rl':
                assert tree.root
                tree.rotate_left(tree.root)
                os.system('cls')
                print(tree)
            case _:
                break

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
        
        # Case 2: Father is red and uncle is black (line)
        if node.parent.is_red() and (uncle is None or uncle.is_black()) and node.parent.side() == node.side():
            pass

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
            if node.side() == Side.LEFT:
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
            if node.side() == Side.LEFT:
                parent.left = child
            else:
                parent.right = child
        else:
            self.root = child

def height(root: Optional[Any]) -> int:
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))  

def graph(root: Any, block_size: int = 2) -> str:
    HEIGHT_FACTOR = 2
    def _walk(node: Optional[Any], height: int, x: int, y: int, matrix: list[list[Any]]):
        if node:
            matrix[y][x] = node
            walk = 2 ** (height - 2)
            _walk(node.left, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
            _walk(node.right, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
    
    h = height(root)
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

if __name__ == "__main__":
    main()
    

