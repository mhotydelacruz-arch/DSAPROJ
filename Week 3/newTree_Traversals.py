"""06 — Tree Traversals: BFS and DFS orders on a binary tree."""
from collections import deque


# DATA STRUCTURE: binary-tree node, with a value and left/right child links.
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# TREE TRAVERSAL — BFS (Breadth-First Search), also called level-order.
# A FIFO queue visits nodes level by level, from the root down.
def bfs_level_order(root):
    if root is None:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return result


# TREE TRAVERSAL — DFS (Depth-First Search), Preorder: Node, Left, Right.
def dfs_preorder(node):
    if node is None:
        return []
    return [node.value] + dfs_preorder(node.left) + dfs_preorder(node.right)


# TREE TRAVERSAL — DFS (Depth-First Search), Inorder: Left, Node, Right.
def dfs_inorder(node):
    if node is None:
        return []
    return dfs_inorder(node.left) + [node.value] + dfs_inorder(node.right)


# TREE TRAVERSAL — DFS (Depth-First Search), Postorder: Left, Right, Node.
def dfs_postorder(node):
    if node is None:
        return []
    return dfs_postorder(node.left) + dfs_postorder(node.right) + [node.value]


if __name__ == "__main__":
    #                 4
    #               /   \
    #              2     6
    #             / \   / \
    #            1   3 5   7
    root = TreeNode(4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(6, TreeNode(5), TreeNode(7)))

    print("BFS level-order:", bfs_level_order(root))
    print("DFS preorder:   ", dfs_preorder(root))
    print("DFS inorder:    ", dfs_inorder(root))
    print("DFS postorder:  ", dfs_postorder(root))
