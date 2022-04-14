"""
-------------------------------------------------------
Linked version of the BST ADT.
-------------------------------------------------------
Author:  David Brown
ID:      999999999
Email:   dbrown@wlu.ca
Section: CP164 A
__updated__ = "2022-03-17"
-------------------------------------------------------
"""
# pylint: disable=protected-access

# Imports
from copy import deepcopy


class _BST_Node:

    def __init__(self, value):
        """
        -------------------------------------------------------
        Initializes a BST node containing value. Child pointers
        are None, height is 1.
        Use: node = _BST_Node(value)
        -------------------------------------------------------
        Parameters:
            value - value for the node (?)
        Returns:
            A _BST_Node object (_BST_Node)
        -------------------------------------------------------
        """
        self._value = deepcopy(value)
        self._left = None
        self._right = None
        self._height = 1
        self._count = 0

    def _update_height(self):
        """
        -------------------------------------------------------
        Updates the height of the current node. _height is 1 plus
        the maximum of the node's (up to) two child heights.
        Use: node._update_height()
        -------------------------------------------------------
        Returns:
            None
        -------------------------------------------------------
        """
        if self._left is None:
            left_height = 0
        else:
            left_height = self._left._height

        if self._right is None:
            right_height = 0
        else:
            right_height = self._right._height

        self._height = max(left_height, right_height) + 1
        return

    def __str__(self):
        """
        USE FOR TESTING ONLY
        -------------------------------------------------------
        Returns node height and value as a string - for debugging.
        -------------------------------------------------------
        """
        return f"h: {self._height}, v: {self._value}"


class BST:

    def __init__(self):
        """
        -------------------------------------------------------
        Initializes an empty BST.
        Use: bst = BST()
        -------------------------------------------------------
        Returns:
            A BST object (BST)
        -------------------------------------------------------
        """
        self._root = None
        self._count = 0

    def is_empty(self):
        """
        -------------------------------------------------------
        Determines if bst is empty.
        Use: b = bst.is_empty()
        -------------------------------------------------------
        Returns:
            True if bst is empty, False otherwise.
        -------------------------------------------------------
        """
        return self._root is None

    def __len__(self):
        """
        -------------------------------------------------------
        Returns the number of nodes in the BST.
        Use: n = len(bst)
        -------------------------------------------------------
        Returns:
            the number of nodes in bst.
        -------------------------------------------------------
        """
        return self._count

    def insert(self, value):
        """
        -------------------------------------------------------
        Inserts a copy of value into bst. Values may appear
        only once in a tree.
        Use: b = bst.insert(value)
        -------------------------------------------------------
        Parameters:
            value - data to be inserted into bst (?)
        Returns:
            inserted - True if value is inserted into bst,
                False otherwise. (boolean)
        -------------------------------------------------------
        """
        self._root, inserted = self._insert_aux(self._root, value)
        return inserted

    def _insert_aux(self, node, value):
        """
        -------------------------------------------------------
        Inserts a copy of value into node.
        Private recursive operation called only by insert.
        Use: node, inserted = self._insert_aux(node, value)
        -------------------------------------------------------
        Parameters:
            node - a bst node (_BST_Node)
            value - data to be inserted into the node (?)
        Returns:
            node - the current node (_BST_Node)
            inserted - True if value is inserted into node,
                False otherwise. (boolean)
        -------------------------------------------------------
        """
        if node is None:
            # Base case: add a new node containing the value.
            node = _BST_Node(value)
            self._count += 1
            inserted = True
        elif value < node._value:
            # General case: check the left subtree.
            node._left, inserted = self._insert_aux(node._left, value)
        elif value > node._value:
            # General case: check the right subtree.
            node._right, inserted = self._insert_aux(node._right, value)
        else:
            # Base case: value is already in the BST.
            inserted = False

        if inserted:
            # Update the node height if any of its children have been changed.
            node._update_height()
        return node, inserted

    def retrieve(self, key):
        """
        -------------------------------------------------------
        Retrieves a copy of a value matching key in bst. (Iterative)
        Use: v = bst.retrieve(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            value - value in the node containing key, otherwise None (?)
        -------------------------------------------------------
        """
        node = self._root
        value = None

        while node is not None and value is None:

            if node._value > key:
                node = node._left
            elif node._value < key:
                node = node._right
            elif node._value == key:
                # for comparison counting
                value = deepcopy(node._value)
        return value

    def remove(self, key):
        """
        -------------------------------------------------------
        Removes a node with a value matching key from the bst.
        Returns the value matched. Updates structure of bst as
        required.
        Use: value = bst.remove(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            value - value matching key if found, otherwise None.
        -------------------------------------------------------
        """
        self._root, value = self._remove_aux(self._root, key)
        return value

    def _remove_aux(self, node, key):
        """
        -------------------------------------------------------
        Attempts to find a value matching key in a BST node. Deletes the node
        if found and returns the sub-tree root.
        Private recursive operation called only by remove.
        Use: node, value = self._remove_aux(node, key)
        -------------------------------------------------------
        Parameters:
            node - a bst node to search for key (_BST_Node)
            key - data to search for (?)
        Returns:
            node - the current node or its replacement (_BST_Node)
            value - value in node containing key, None otherwise.
        -------------------------------------------------------
        """
        if node is None:
            # Base Case: the key is not in the tree.
            value = None
        elif key < node._value:
            # Search the left subtree.
            node._left, value = self._remove_aux(node._left, key)
        elif key > node._value:
            # Search the right subtree.
            node._right, value = self._remove_aux(node._right, key)
        else:
            # Value has been found.
            value = node._value
            self._count -= 1
            # Replace this node with another node.
            if node._left is None and node._right is None:
                # node has no children.
                node = None
            elif node._left is None:
                # node has no left child.
                node = node._right
            elif node._right is None:
                # node has no right child.
                node = node._left
            else:
                # Node has two children
                if node._left._right is None:
                    # left child is replacement node
                    repl_node = node._left
                else:
                    # find replacement node in right subtree of left node
                    repl_node = self._delete_node_left(node._left)
                    repl_node._left = node._left

                repl_node._right = node._right
                node = repl_node

        if node is not None and value is not None:
            # If the value was found, update the ancestor heights.
            node._update_height()
        return node, value

    def _delete_node_left(self, parent):
        """
        -------------------------------------------------------
        Finds a replacement node for a node to be removed from the tree.
        Private operation called only by _remove_aux.
        Use: repl_node = self._delete_node_left(parent)
        -------------------------------------------------------
        Parameters:
            parent - node to search for largest value (_BST_Node)
        Returns:
            repl_node - the node that replaces the deleted node. This node
                is the node with the maximum value in the deleted node's left
                subtree (_BST_Node)
        -------------------------------------------------------
        """
        child = parent._right

        if child._right is None:
            # child has largest value in left subtree
            repl_node = child
            # move child's left tree up
            parent._right = child._left
        else:
            repl_node = self._delete_node_left(child)

        # Recursively update all parent node heights
        parent._update_height()
        return repl_node

    def height(self):
        """
        -------------------------------------------------------
        Returns the maximum height of a BST, i.e. the length of the
        longest path from root to a leaf node in the tree.
        Use: h = bst.height()
        -------------------------------------------------------
        Returns:
            h - maximum height of bst (int)
        -------------------------------------------------------
        """
        if self._root is None:
            h = 0
        else:
            h = self._root._height
        return h

    def is_identical(self, other):
        """
        ---------------------------------------------------------
        Determines whether two BSTs are identical.
        Use: b = bst.is_identical(other)
        -------------------------------------------------------
        Parameters:
            other - another bst (BST)
        Returns:
            identical - True if this bst contains the same values
            in the same order as other, otherwise returns False (boolean)
        -------------------------------------------------------
        """
        if self._count != other._count:
            identical = False
        else:
            identical = self._is_identical_aux(self._root, other._root)
        return identical

    def _is_identical_aux(self, node1, node2):
        """
        ---------------------------------------------------------
        Determines whether two subtrees are identical.
        Use: b = self._is_identical_aux(node1, node2)
        -------------------------------------------------------
        Parameters:
            node1 - node of the current BST (_BST_Node)
            node2 - node of the rs BST (_BST_Node)
        Returns:
            identical - True if this subtree contains the same values as rs
                subtree in the same order, otherwise returns False (boolean)
        -------------------------------------------------------
        """
        if node1 is None and node2 is None:
            # Reached a bottom of the tree.
            identical = True
        elif node1 is not None and node2 is not None \
                and node1._value == node2._value and node1._height == node2._height:
            identical = self._is_identical_aux(node1._left, node2._left) \
                and self._is_identical_aux(node1._right, node2._right)
        else:
            identical = False
        return identical

    def max(self):
        """
        -------------------------------------------------------
        Finds the maximum value in BST. (Iterative algorithm)
        Use: value = bst.max()
        -------------------------------------------------------
        Returns:
            value - a copy of the maximum value in the BST (?)
        -------------------------------------------------------
        """
        assert self._root is not None, "Cannot find maximum of an empty BST"
        # Find the node containing the largest _value.
        # (It is the right-most node.)
        node = self._root

        while node._right is not None:
            node = node._right

        value = deepcopy(node._value)
        return value

    def max_r(self):
        """
        ---------------------------------------------------------
        Returns the largest value in a bst. (Recursive algorithm)
        Use: value = bst.max_r()
        ---------------------------------------------------------
        Returns:
            value - a copy of the maximum value in the BST (?)
        ---------------------------------------------------------
        """
        assert self._root is not None, "Cannot find maximum of an empty BST"

        value = self._max_aux(self._root)
        return value

    def _max_aux(self, node):
        """
        ---------------------------------------------------------
        Returns the largest value in a BST node. (Recursive algorithm)
        Use: v = self._max_aux(node)
        ---------------------------------------------------------
        Parameters:
            node - linked BST node (_BST_Node)
        Returns:
            value - a copy of the largest value in the node subtree (?)
        ---------------------------------------------------------
        """
        # Find the node containing the largest _value.
        # (It is the right-most node.)
        if node._right is None:
            value = deepcopy(node._value)
        else:
            value = self._max_aux(node._right)
        return value

    def min(self):
        """
        -------------------------------------------------------
        Finds the minimum value in BST. (Iterative algorithm)
        Use: value = bst.min()
        -------------------------------------------------------
        Returns:
            value - a copy of the minimum value in the BST (?)
        -------------------------------------------------------
        """
        assert self._root is not None, "Cannot find minimum of an empty BST"
        # Find the node containing the smallest _value.
        # (It is the left-most node.)
        node = self._root

        while node._left is not None:
            node = node._left

        value = deepcopy(node._value)
        return value

    def min_r(self):
        """
        ---------------------------------------------------------
        Returns the minimum value in a bst. (Recursive algorithm)
        Use: value = bst.min_r()
        ---------------------------------------------------------
        Returns:
            value - a copy of the minimum value in the BST (?)
        ---------------------------------------------------------
        """
        assert self._root is not None, "Cannot find minimum of an empty BST"

        value = self._min_aux(self._root)
        return value

    def _min_aux(self, node):
        """
        ---------------------------------------------------------
        Returns the minimum value in a BST node. (Recursive algorithm)
        Use: v = self._max_aux(node)
        ---------------------------------------------------------
        Parameters:
            node - linked BST node (_BST_Node)
        Returns:
            value - a copy of the minimum value in the node subtree (?)
        ---------------------------------------------------------
        """
        # Find the node containing the minimum _value.
        # (It is the left-most node.)
        if node._left is None:
            value = deepcopy(node._value)
        else:
            value = self._min_aux(node._left)
        return value

    def leaf_count(self):
        """
        ---------------------------------------------------------
        Returns the number of leaves (nodes with no children) in bst.
        Use: n = bst.leaf_count()
        (Recursive algorithm)
        ---------------------------------------------------------
        Returns:
            count - number of nodes with no children in bst (int)
        ---------------------------------------------------------
        """
        count = self._leaf_count_aux(self._root)
        return count

    def _leaf_count_aux(self, node):
        """
        ---------------------------------------------------------
        Returns the number of leaves (nodes with no children) in bst.
        Use: count = bst.leaf_count()
        ---------------------------------------------------------
        Parameters:
            node - a BST node (_BST_Node)
        Returns:
            count - number of nodes with no children below node (int)
        ---------------------------------------------------------
        """
        if node is None:
            count = 0
        elif node._left is None and node._right is None:
            # Base case: node has no children.
            count = 1
        else:
            count = self._leaf_count_aux(node._left) + \
                self._leaf_count_aux(node._right)
        return count

    def two_child_count(self):
        """
        ---------------------------------------------------------
        Returns the number of the three types of nodes in a BST.
        Use: count = bst.two_child_count()
        -------------------------------------------------------
        Returns:
            count - number of nodes with two children in bst (int)
        ----------------------------------------------------------
        """
        return self._two_child_count_aux(self._root)

    def _two_child_count_aux(self, node):
        """
        ---------------------------------------------------------
        Returns the number of types of nodes in a BST node.
        -------------------------------------------------------
        Parameters:
            node - a BST node (_BST_Node)
        Returns:
            count - number of nodes with two children in bst (int)
        ----------------------------------------------------------
        """
        if node is None:
            # Base case: node is empty.
            count = 0
        elif node._left is not None and node._right is not None:
            # General case: node has two children.
            count = 1 + self._two_child_count_aux(node._left) + \
                self._two_child_count_aux(node._right)
        else:
            # General case: node has one child.
            count = self._two_child_count_aux(node._left) + \
                self._two_child_count_aux(node._right)
        return count

    def one_child_count(self):
        """
        ---------------------------------------------------------
        Returns the number of the three types of nodes in a BST.
        Use: count = bst.one_child_count()
        -------------------------------------------------------
        Returns:
            count - number of nodes with one child in bst (int)
        ----------------------------------------------------------
        """
        return self._one_child_count_aux(self._root)

    def _one_child_count_aux(self, node):
        """
        ---------------------------------------------------------
        Returns the number of types of nodes in a BST node.
        -------------------------------------------------------
        Parameters:
            node - a BST node (_BST_Node)
        Returns:
            count - number of nodes with one child in bst (int)
        ----------------------------------------------------------
        """
        if node is None:
            # Base case: empty node..
            count = 0
        elif node._left is None and node._right is not None:
            # General case: node has one child.
            count = 1 + self._one_child_count_aux(node._right)
        elif node._left is not None and node._right is None:
            # General case: node has one child.
            count = 1 + self._one_child_count_aux(node._left)
        else:
            # General case: node has two children.
            count = self._one_child_count_aux(node._left) + \
                self._one_child_count_aux(node._right)
        return count

    def is_balanced(self):
        """
        ---------------------------------------------------------
        Returns whether a bst is balanced, i.e. the difference in
        height between all the bst's node's left and right subtrees is <= 1.
        Use: b = bst.is_balanced()
        ---------------------------------------------------------
        Returns:
            has_balanced - True if the bst is has_balanced, False otherwise (boolean)
        ---------------------------------------------------------
        """
        has_balanced = self._is_balanced_aux(self._root)
        return has_balanced

    def _is_balanced_aux(self, node):
        """
        ---------------------------------------------------------
        Determines whether the BST is is_balanced.
        Private operation called only by _is_balanced_aux.
        Use: b = self._balanced_aux(node)
        ---------------------------------------------------------
        Parameters:
            node - the node to check the balance of (_BST_Node)
        Returns:
            has_balanced - True if node is is has_balanced, False otherwise (boolean)
        ---------------------------------------------------------
        """
        if node is None or node._height == 1:
            # Base case: node is empty or a leaf, so no children.
            has_balanced = True
        elif abs(self._node_height(node._left) -
                 self._node_height(node._right)) > 1:
            # Base case: left or right subtree is too deep.
            has_balanced = False
        else:
            # General case: check the children of node.
            has_balanced = self._is_balanced_aux(node._left) and \
                self._is_balanced_aux(node._right)
        return has_balanced

    def _node_height(self, node):
        """
        ---------------------------------------------------------
        Helper function to determine the height of node - handles empty node.
        Private operation called only by _is_valid_aux.
        Use: h = self._node_height(node)
        ---------------------------------------------------------
        Parameters:
            node - the node to get the height of (_BST_Node)
        Returns:
            height - 0 if node is None, node._height otherwise (int)
        ---------------------------------------------------------
        """
        if node is None:
            height = 0
        else:
            height = node._height
        return height

    def retrieve_r(self, key):
        """
        -------------------------------------------------------
        Retrieves a _value in a BST. (Recursive)
        Use: v = bst.retrieve(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            value - If bst contains key, returns value, else returns None.
        -------------------------------------------------------
        """
        # Find the node containing the key _value.
        value = self._retrieve_r_aux(self._root, key)
        return value

    def _retrieve_r_aux(self, current, key):
        """
        -------------------------------------------------------
        Retrieves a _value in a BST.
        -------------------------------------------------------
        Parameters:
            current - a bst node (_BST_Node)
            key - data to search for (?)
        Returns:
            value - contains key, else returns None (?)
        -------------------------------------------------------
        """
        if current is None:
            # Base case: at bottom of tree and key not found.
            value = None
        else:
            if key < current._value:
                value = self._retrieve_r_aux(current._left, key)
            elif key > current._value:
                value = self._retrieve_r_aux(current._right, key)
            else:
                value = deepcopy(current._value)
        return value

    def is_valid(self):
        """
        ---------------------------------------------------------
        Determines if a tree is a valid BST, i.e. the values in all left nodes
        are smaller than their parent, and the values in all right nodes are
        larger than their parent, and height of any node is 1 + max height of
        its children.
        Use: b = bst.is_valid()
        ---------------------------------------------------------
        Returns:
            valid - True if tree is a BST, False otherwise (boolean)
        ---------------------------------------------------------
        """
        valid = self._is_valid_aux(self._root, None, None)
        return valid

    def _is_valid_aux(self, node, min_node, max_node):
        """
        ---------------------------------------------------------
        Private recursive method to determine the BST validity of node,
        used only by is_valid.
        Use: valid = self._is_valid_aux(node, min_node, max_node)
        ---------------------------------------------------------
        Parameters:
            node - a binary tree node (_BST_Node)
            min_node - the node with the minimum value for the current tree (_BST_Node)
            max_node - the node with the maximum value for the current tree (_BST_Node)
        Returns:
            valid - True if node is root of a valid BST, False otherwise (boolean)
        ---------------------------------------------------------
        """
        if node is None:
            valid = True
        elif min_node is not None and node._value <= min_node._value:
            # print("BST left value violation at value: {}".format(node._value))
            valid = False
        elif max_node is not None and node._value >= max_node._value:
            # print("BST right value violation at value: {}".format(node._value))
            valid = False
        elif node._height != max(self._node_height(node._left), self._node_height(node._right)) + 1:
            # print("BST height violation at value: {}".format(node._value))
            valid = False
        else:
            # node becomes max node of left tree, min node of right tree
            valid = self._is_valid_aux(node._left, min_node, node) \
                and self._is_valid_aux(node._right, node, max_node)
        return valid

    def inorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in inorder order.
        Use: a = bst.inorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in inorder (list of ?)
        -------------------------------------------------------
        """
        a = []
        self._inorder_aux(self._root, a)
        return a

    def _inorder_aux(self, node, a):
        """
        ---------------------------------------------------------
        Traverses node subtree in inorder. a contains the contents of
        node and its children in inorder.
        Private recursive operation called only by inorder.
        Use: self._inorder_aux(node, a)
        ---------------------------------------------------------
        Parameters:
            node - an BST node (_BST_Node)
            a - target list of data (list of ?)
        Returns:
            None
        ---------------------------------------------------------
        """
        if node is not None:
            self._inorder_aux(node._left, a)
            a.append(deepcopy(node._value))
            self._inorder_aux(node._right, a)
        return

    def preorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in preorder order.
        Use: a = bst.preorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in preorder (list of ?)
        -------------------------------------------------------
        """
        a = []
        self._preorder_aux(self._root, a)
        return a

    def _preorder_aux(self, node, a):
        """
        ---------------------------------------------------------
        Traverses node subtree in preorder. a contains the contents of
        node and its children in preorder.
        Private recursive operation called only by preorder.
        Use: self._preorder_aux(node, a)
        ---------------------------------------------------------
        Parameters:
            node - an BST node (_BST_Node)
            a - target of data (list of ?)
        Returns:
            None
        ---------------------------------------------------------
        """
        if node is not None:
            a.append(deepcopy(node._value))
            self._preorder_aux(node._left, a)
            self._preorder_aux(node._right, a)
        return

    def postorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in postorder order.
        Use: a = bst.postorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in postorder (list of ?)
        -------------------------------------------------------
        """
        a = []
        self._postorder_aux(self._root, a)
        return a

    def _postorder_aux(self, node, a):
        """
        ---------------------------------------------------------
        Traverses node subtree in postorder. a contains the contents of
        node and its children in postorder.
        Private recursive operation called only by postorder.
        Use: self._postorder_aux(node, a)
        ---------------------------------------------------------
        Parameters:
            node - an BST node (_BST_Node)
            a - target of data (list of ?)
        Returns:
            None
        ---------------------------------------------------------
        """
        if node is not None:
            self._postorder_aux(node._left, a)
            self._postorder_aux(node._right, a)
            a.append(deepcopy(node._value))
        return

    def levelorder(self):
        """
        -------------------------------------------------------
        Copies the contents of the tree in levelorder order to a list.
        Use: values = bst.levelorder()
        -------------------------------------------------------
        Returns:
            values - a list containing the values of bst in levelorder.
            (list of ?)
        -------------------------------------------------------
        """
        values = []

        if self._root is not None:
            # Put the nodes for one level into a queue.
            queue = []
            queue.append(self._root)

            while len(queue) > 0:
                # Add a copy of the data to the sublist
                node = queue.pop(0)
                values.append(deepcopy(node._value))

                if node._left is not None:
                    queue.append(node._left)
                if node._right is not None:
                    queue.append(node._right)
        return values

    def count(self):
        """
        ---------------------------------------------------------
        Returns the number of nodes in a BST.
        Use: number = bst.count()
        -------------------------------------------------------
        Returns:
            number - count of nodes in tree (int)
        ----------------------------------------------------------
        """
        number = self._count_aux(self._root)
        return number

    def _count_aux(self, node):
        """
        ---------------------------------------------------------
        Returns the number of nodes in a BST subtree.
        -------------------------------------------------------
        Parameters:
            node - a BST node (_BST_Node)
        Returns:
            number - count of nodes in the current subtree (int)
        ----------------------------------------------------------
        """
        if node is None:
            # Base case: node does not exist
            number = 0
        else:
            # General case: node exists.
            number = 1 + self._count_aux(node._left) + \
                self._count_aux(node._right)
        return number

    def __iter__(self):
        """
        -------------------------------------------------------
        Generates a Python iterator. Iterates through a BST node
        in level order.
        Use: for v in bst:
        -------------------------------------------------------
        Returns:
            yields
            value - the values in the BST node and its children (?)
        -------------------------------------------------------
        """
        if self._root is not None:
            # Put the nodes for one level into a queue.
            queue = []
            queue.append(self._root)

            while len(queue) > 0:
                # Add a copy of the data to the sublist
                node = queue.pop(0)
                yield node._value

                if node._left is not None:
                    queue.append(node._left)
                if node._right is not None:
                    queue.append(node._right)
