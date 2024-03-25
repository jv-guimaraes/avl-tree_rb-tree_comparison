class Node:
    def __init__(self, key, parent=None, color='Red'):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None
        self.color = color


class RedBlackTree:
    def __init__(self):
        self.nil = Node(None, color='Black')  # Sentinel node
        self.root = self.nil

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.nil
        new_node.right = self.nil

        parent = None
        current = self.root

        while current != self.nil:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = 'Red'
        self._insert_fixup(new_node)

    def _insert_fixup(self, node):
        while node.parent.color == 'Red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 'Red':
                    node.parent.color = 'Black'
                    uncle.color = 'Black'
                    node.parent.parent.color = 'Red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = 'Black'
                    node.parent.parent.color = 'Red'
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 'Red':
                    node.parent.color = 'Black'
                    uncle.color = 'Black'
                    node.parent.parent.color = 'Red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = 'Black'
                    node.parent.parent.color = 'Red'
                    self._left_rotate(node.parent.parent)

        self.root.color = 'Black'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def search(self, key):
        current = self.root
        while current != self.nil and key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current

    def transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    def remove(self, key):
        node = self.search(key)
        if node == self.nil:
            return
        y = node
        y_original_color = y.color
        if node.left == self.nil:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.nil:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == 'Black':
            self._remove_fixup(x)

    def _remove_fixup(self, x):
        while x != self.root and x.color == 'Black':
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == 'Red':
                    sibling.color = 'Black'
                    x.parent.color = 'Red'
                    self._left_rotate(x.parent)
                    sibling = x.parent.right
                if sibling.left.color == 'Black' and sibling.right.color == 'Black':
                    sibling.color = 'Red'
                    x = x.parent
                else:
                    if sibling.right.color == 'Black':
                        sibling.left.color = 'Black'
                        sibling.color = 'Red'
                        self._right_rotate(sibling)
                        sibling = x.parent.right
                    sibling.color = x.parent.color
                    x.parent.color = 'Black'
                    sibling.right.color = 'Black'
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == 'Red':
                    sibling.color = 'Black'
                    x.parent.color = 'Red'
                    self._right_rotate(x.parent)
                    sibling = x.parent.left
                if sibling.right.color == 'Black' and sibling.left.color == 'Black':
                    sibling.color = 'Red'
                    x = x.parent
                else:
                    if sibling.left.color == 'Black':
                        sibling.right.color = 'Black'
                        sibling.color = 'Red'
                        self._left_rotate(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = 'Black'
                    sibling.left.color = 'Black'
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = 'Black'

    def inorder_traversal(self, node):
        if node != self.nil:
            self.inorder_traversal(node.left)
            print(node.key, end=" ")
            self.inorder_traversal(node.right)


# Example usage:

# Create a new red-black tree
rb_tree = RedBlackTree()

# Insert some values
rb_tree.insert(7)
rb_tree.insert(3)
rb_tree.insert(18)
rb_tree.insert(10)
rb_tree.insert(22)
rb_tree.insert(8)
rb_tree.insert(11)

# Search for a value
search_result = rb_tree.search(10)
if search_result != rb_tree.nil:
    print("Found:", search_result.key)
else:
    print("Not found")

# Remove a value
rb_tree.remove(10)

# Inorder traversal to check the tree structure
print("Inorder Traversal after removal:")
rb_tree.inorder_traversal(rb_tree.root)
