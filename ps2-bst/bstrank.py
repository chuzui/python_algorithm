import bstsize

class BST(bstsize.BST):
    """
    Adds rank method to BST, starting with code from bstsize.
    """

    def rank(self, key):
        """
        Takes a key, and returns the number of elements less than or
        equal to the key.  Starting at the root, it finds the location
        of the key in the tree, adding the sizes of left-subtrees,
        because those contain smaller elements
        """
        rank = 0 # a running sum of nodes smaller than key
        node = self.root
        while node is not None:
            if key == node.key: # we have found the key, so we add the
                                # size of its left subtree (plus
                                # itself)
                rank += bstsize.size(node.left) + 1
                return rank
            elif key < node.key: # we have found a larger node, so we
                                 # go down its left child
                node = node.left
            else: # we have found a smaller node, so we go down its
                  # right child, and add the size of its left subtree
                  # (plus itself)
                rank += bstsize.size(node.left) + 1
                node = node.right
        return rank
