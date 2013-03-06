import bstsize

class BST(bstsize.BST):
    """
    Adds select method to BST, starting with code from bstsize.   
    """
    
    def select(self, index):
        """
        Takes a 1-based index, and returns the element at that index,
        or None if the index is out-of-bounds.
        """
        if index > bstsize.size(self.root) or index <= 0:
            return None
        node = self.root;
        remainder_index = index;
        while remainder_index >= 0:
            if remainder_index == bstsize.size(node.left) + 1:
                return node
            elif remainder_index > bstsize.size(node.left) + 1:
                remainder_index = remainder_index - (bstsize.size(node.left) + 1)
                node = node.right
            else:
                node = node.left
        return None
