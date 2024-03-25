from typing import Optional, Any
from io import StringIO

class Node:
    def __init__(self, value: int):
        self.value: int = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height: int = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert_key(self, value: int):
        self.root = insert(self.root, value)

    def inorder(self, root: Optional[Node]):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)
    
    def graph(self, block_size: int = 2, show_parent: bool = False) -> str:
        HEIGHT_FACTOR = 2
        def __walk(node: Optional[Node], height: int, x: int, y: int, matrix: list[list[Any]]):
            if node:
                matrix[y][x] = node
                walk = 2 ** (height - 2)
                __walk(node.left, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
                __walk(node.right, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
        
        h = height(self.root)
        w = 2 ** h - 1
        matrix: list[list[Any]] = [[None for _ in range(w)] for _ in range(h * HEIGHT_FACTOR)]
        __walk(self.root, h, 2 ** (h - 1) - 1, 0, matrix)
        
        buffer = StringIO()
        for row in matrix:
            for node in row:
                if node is None:
                    buffer.write((' ' * block_size) + ' '); continue
                if show_parent and node.parent:
                    buffer.write(f'{node.value}({node.parent.value}) ')
                else:
                    buffer.write(f'{node.value} ')
            buffer.write('\n')
        
        return buffer.getvalue()


def height(node: Optional[Node]) -> int:
    if not node:
        return 0
    return node.height

def balance(node: Optional[Node]) -> int:
    if not node:
        return 0
    return height(node.left) - height(node.right)


def rotate_right(y: Node):
    assert(y.left)
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    y.height = 1 + max(height(y.left), height(y.right))
    x.height = 1 + max(height(x.left), height(x.right))

    return x

def rotate_left(x: Node):
    assert(x.right)
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))

    return y

def insert(root: Optional[Node], value: int) -> Optional[Node]:
    if not root:
        return Node(value)

    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)

    root.height = 1 + max(height(root.left), height(root.right))

    bf = balance(root)

    if bf > 1:
        assert(root.left)
        if value < root.left.value:
            return rotate_right(root)
        else:
            root.left = rotate_left(root.left)
            return rotate_right(root)
    if bf < -1:
        assert(root.right)
        if value > root.right.value:
            return rotate_left(root)
        else:
            root.right = rotate_right(root.right)
            return rotate_left(root)

    return root