from typing import Optional, Any
from io import StringIO
from dataclasses import dataclass

@dataclass
class Node:
    value: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    height: int = 1        
         
class AVLTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value: int):
        
        def _insert(root: Optional[Node], value: int) -> Optional[Node]:
            if not root:
                return Node(value)

            if value < root.value:
                root.left = _insert(root.left, value)
            else:
                root.right = _insert(root.right, value)

            root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
            
            return self._balance(root)
        
        if self._search_node(value) is None:
            self.root = _insert(self.root, value)
    
    def _search_node(self, value: int) -> Optional[int]:
        
        def _search(root: Optional[Node], value: int) -> Optional[Node]:
            if not root or root.value == value:
                return root
            
            if value < root.value:
                return _search(root.left, value)
            else:
                return _search(root.right, value)
        
        res = _search(self.root, value)
        return res.value if res else None

    def contains(self, value: int) -> bool:
        return self._search_node(value) is not None
        
    def delete(self, value: int):

        def _delete(root: Optional[Node], value: int) -> Optional[Node]:
            if not root:
                return None

            if value < root.value:
                root.left = _delete(root.left, value)
            elif value > root.value:
                root.right = _delete(root.right, value)
            else: #Encontrou o valor a ser deletado
                if not root.left:  
                    return root.right
                elif not root.right: 
                    return root.left
                else: 
                    successor = root.right
                    while successor.left:
                        successor = successor.left
                    root.value = successor.value
                    root.right = _delete(root.right, successor.value)

            root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

            return self._balance(root)

        # old_root = self.root
        self.root = _delete(self.root, value)

        # If the root has changed, the removal was successful
        # return old_root != self.root
    
    def _get_height(self, node: Optional[Node]) -> int:
        if not node: return 0
        return node.height
    
    def _get_bf(self, node: Optional[Node]) -> int:
        if not node: return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, y: Node) -> Node:
        assert y.left
        x = y.left
        z = x.right

        x.right = y
        y.left = z

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _rotate_left(self, x: Node) -> Node:
        assert x.right
        y = x.right
        z = y.left

        y.left = x
        x.right = z

        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y
   
    def _balance(self, root: Node) -> Node:
        bf = self._get_bf(root)
        if bf > 1:
            assert root.left
            if self._get_bf(root.left) >= 0:
                return self._rotate_right(root)
            else:
                root.left = self._rotate_left(root.left)
                return self._rotate_right(root)
        elif bf < -1:
            assert root.right
            if self._get_bf(root.right) <= 0:
                return self._rotate_left(root)
            else:
                root.right = self._rotate_right(root.right)
                return self._rotate_left(root)

        return root

    def graph(self, block_size: int = 2) -> str:
        HEIGHT_FACTOR = 2
        def _walk(node: Optional[Node], height: int, x: int, y: int, matrix: list[list[Any]]):
            if node:
                matrix[y][x] = node
                walk = 2 ** (height - 2)
                _walk(node.left, height - 1, x - walk, y + 1 * HEIGHT_FACTOR, matrix)
                _walk(node.right, height - 1, x + walk, y + 1 * HEIGHT_FACTOR, matrix)
        
        h = self._get_height(self.root)
        w = 2 ** h - 1
        matrix: list[list[Any]] = [[None for _ in range(w)] for _ in range(h * HEIGHT_FACTOR)]
        _walk(self.root, h, 2 ** (h - 1) - 1, 0, matrix)
        
        buffer = StringIO()
        for row in matrix:
            for node in row:
                if node is None:
                    buffer.write((' ' * block_size) + ' '); continue
                else:
                    buffer.write(f'{node.value} ')
            buffer.write('\n')
        
        return buffer.getvalue()
