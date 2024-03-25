from dataclasses import dataclass
from typing import Optional, Any
from io import StringIO

@dataclass
class Node:
    value: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None

    def __str__(self) -> str:
        left_value = self.left.value if self.left else None
        right_value = self.right.value if self.right else None
        return f'({self.value}, l: {left_value}, r: {right_value})'

@dataclass
class AVLTree:
    root: Optional['Node']

    def __init__(self) -> None:
        self.root = None

    def insert(self, value: int) -> None:
        if self.root is None:
            self.root = Node(value)
            return
        
        def __insert(node: Node, value: int):
            if value == node.value:
                return
            elif value < node.value:
                if node.left is None:
                    node.left = Node(value)
                else:
                    __insert(node.left, value)
            else:
                if node.right is None:
                    node.right = Node(value)
                else:
                    __insert(node.right, value)
        
        __insert(self.root, value)
    
    def search(self, value: int) -> Optional[int]:
        def __search(node: Optional[Node], value: int) -> Optional[int]:
            if not node:
                return None
            elif node.value == value:
                return value
            else:
                return __search(node.left, value) or __search(node.right, value)
        return __search(self.root, value)    
    
    def height(self) -> int:
        def __height(node: Optional[Node]) -> int:
            if node is None:
                return 0
            return max(__height(node.left), __height(node.right)) + 1

        return __height(self.root)
    
    def dfs_print(self) -> None:
        def __print(node: Optional[Node]):
            if node:
                print(f'{node.value} ', end='')
                __print(node.left)
                __print(node.right)
        __print(self.root); print()

    def graph(self) -> str:
        HEIGHT_FACTOR = 2
        def __walk(node: Optional[Node], height: int, x: int, y: int, matrix: list[list[Any]]):
            if node:
                matrix[y][x] = node.value
                walk = 2 ** (height - 2)
                __walk(node.left, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
                __walk(node.right, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
        
        height = self.height()
        width = 2 ** height - 1
        matrix: list[list[Any]] = [['  ' for _ in range(width)] for _ in range(height * HEIGHT_FACTOR)]
        __walk(self.root, height, 2 ** (height - 1) - 1, 0, matrix)
        
        buffer = StringIO()
        for row in matrix:
            for value in row:
                buffer.write(f'{value} ')
            buffer.write('\n')
        
        return buffer.getvalue()

