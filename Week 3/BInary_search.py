"""07 — Binary Search: fish and poultry stored in an AVL Binary Search Tree.

Fish key: (growth-stage rank, animal ID).
Poultry key: (age in days, animal ID).
Health is node data, not part of the key, so it can be mutated without
breaking BST ordering. Harvest deletes a mature animal and AVL rotations
rebalance the remaining tree.
"""
from dataclasses import dataclass


# DATA STRUCTURE: OOP animal record stored as the payload in a BST node.
@dataclass
class Animal:
    animal_id: int
    species: str
    age_days: int
    health: int = 80

    @property
    def stage(self):
        if self.species == "fish":
            if self.age_days < 2:
                return "Fingerling"
            if self.age_days < 4:
                return "Juvenile"
            return "Market-size"
        if self.age_days < 2:
            return "Chick"
        if self.age_days < 4:
            return "Pullet"
        return "Layer"

    @property
    def stage_rank(self):
        if self.age_days < 2:
            return 0
        if self.age_days < 4:
            return 1
        return 2


# DATA STRUCTURE: binary-tree node with left/right links and a height for AVL balancing.
class BSTNode:
    def __init__(self, animal):
        self.animal = animal
        self.left = None
        self.right = None
        self.height = 1


# DATA STRUCTURE: AVL Binary Search Tree, a self-balancing Binary Search Tree.
class AnimalBST:
    def __init__(self, species):
        if species not in ("fish", "poultry"):
            raise ValueError("species must be 'fish' or 'poultry'")
        self.species = species
        self.root = None

    def key_for(self, animal):
        if self.species == "fish":
            return animal.stage_rank, animal.animal_id
        return animal.age_days, animal.animal_id

    @staticmethod
    def _height(node):
        return node.height if node else 0

    def _refresh(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return node

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, root):
        pivot = root.left
        root.left = pivot.right
        pivot.right = root
        self._refresh(root)
        return self._refresh(pivot)

    def _rotate_left(self, root):
        pivot = root.right
        root.right = pivot.left
        pivot.left = root
        self._refresh(root)
        return self._refresh(pivot)

    def _rebalance(self, node):
        if node is None:
            return None
        self._refresh(node)
        balance = self._balance_factor(node)
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, animal):
        if animal.species != self.species:
            raise ValueError("animal species does not match this BST")
        self.root = self._insert(self.root, animal)

    def _insert(self, node, animal):
        if node is None:
            return BSTNode(animal)
        key = self.key_for(animal)
        node_key = self.key_for(node.animal)
        if key < node_key:
            node.left = self._insert(node.left, animal)
        elif key > node_key:
            node.right = self._insert(node.right, animal)
        else:
            raise ValueError("duplicate BST key")
        return self._rebalance(node)

    # BINARY SEARCH: compare keys and follow one child per step; O(log n) in an AVL tree.
    def search(self, key):
        node = self.root
        while node is not None:
            node_key = self.key_for(node.animal)
            if key == node_key:
                return node.animal
            if key < node_key:
                node = node.left
            else:
                node = node.right
        return None

    # NODE MUTATION: health is not in the key, so changing it preserves BST ordering.
    def mutate_health(self, key, amount):
        animal = self.search(key)
        if animal is None:
            return None
        animal.health = max(0, min(100, animal.health + amount))
        return animal.health

    # BINARY SEARCH TREE DELETION: remove by key, then rebalance using AVL rotations.
    def delete(self, key):
        removed = self.search(key)
        if removed is not None:
            self.root = self._delete(self.root, key)
        return removed

    def _delete(self, node, key):
        if node is None:
            return None
        node_key = self.key_for(node.animal)
        if key < node_key:
            node.left = self._delete(node.left, key)
        elif key > node_key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.animal = successor.animal
            node.right = self._delete(node.right, self.key_for(successor.animal))
        return self._rebalance(node)

    # TREE TRAVERSAL: DFS Inorder returns animals in ascending BST-key order.
    def inorder(self):
        result = []

        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.animal)
                visit(node.right)

        visit(self.root)
        return result

    def validate(self):
        """Check binary-search ordering, stored heights, and AVL balance."""
        def check(node, lower=None, upper=None):
            if node is None:
                return 0
            key = self.key_for(node.animal)
            assert lower is None or lower < key
            assert upper is None or key < upper
            left_height = check(node.left, lower, key)
            right_height = check(node.right, key, upper)
            assert node.height == 1 + max(left_height, right_height)
            assert abs(left_height - right_height) <= 1
            return node.height

        check(self.root)
        return True


if __name__ == "__main__":
    pond = AnimalBST("fish")
    for animal in [
        Animal(1, "fish", 0, 88),
        Animal(2, "fish", 2, 84),
        Animal(3, "fish", 4, 92),
        Animal(4, "fish", 5, 90),
    ]:
        pond.insert(animal)

    print("Fish in BST order:", [(a.animal_id, a.stage) for a in pond.inorder()])
    print("Search for market-size fish:", pond.search((2, 3)))
    print("Feed fish #2; new health:", pond.mutate_health((1, 2), 12))
    harvested = pond.delete((2, 3))
    print("Harvest/delete:", harvested)
    print("BST/AVL valid after deletion:", pond.validate())
