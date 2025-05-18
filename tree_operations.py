class TreeNode:
    def __init__(self, key):
        self.data = key
        self.left = None
        self.right = None
        self.height = 1

def getHeight(node):
    return node.height if node else 0

def getBalance(node):
    return getHeight(node.left) - getHeight(node.right) if node else 0

def rightRotate(z):
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3
    z.height = 1 + max(getHeight(z.left), getHeight(z.right))
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))
    return y

def leftRotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(getHeight(z.left), getHeight(z.right))
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))
    return y

def insert_bst_iter(root, key):
    new_node = TreeNode(key)
    if root is None:
        return new_node
    current = root
    while True:
        if key < current.data:
            if current.left is None:
                current.left = new_node
                break
            current = current.left
        else:
            if current.right is None:
                current.right = new_node
                break
            current = current.right
    return root

def insert_avl_iter(root, key):
    if not root:
        return TreeNode(key)

    stack = []
    current = root

    while True:
        stack.append(current)
        if key < current.data:
            if current.left is None:
                current.left = TreeNode(key)
                break
            current = current.left
        else:
            if current.right is None:
                current.right = TreeNode(key)
                break
            current = current.right

    while stack:
        node = stack.pop()
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))
        balance = getBalance(node)

        if balance > 1:
            if key < node.left.data:
                node = rightRotate(node)
            else:
                node.left = leftRotate(node.left)
                node = rightRotate(node)
        elif balance < -1:
            if key > node.right.data:
                node = leftRotate(node)
            else:
                node.right = rightRotate(node.right)
                node = leftRotate(node)

        if stack:
            parent = stack[-1]
            if parent.left == node or (parent.left and parent.left.data == node.data):
                parent.left = node
            else:
                parent.right = node
        else:
            root = node
    return root 