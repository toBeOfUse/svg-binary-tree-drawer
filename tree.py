import math


class ListBasedBinaryTree:
    """List-based binary tree that provides the functions that our drawing algorithm
    will need. The root of the tree is considered to be at level 1."""

    def __init__(self, listRepresentation: list):
        """
        Initializes a binary tree based on a list. The list should have None values
        to signify non-existant nodes.
        """
        self.list = listRepresentation

    @property
    def height(self):
        return math.ceil(math.log2(len(self.list)))

    @staticmethod
    def getMaxNodeCountByLevel(level: int):
        return 2**(level - 1)

    def getNodesByLevel(self, level: int):
        start = sum((self.getMaxNodeCountByLevel(i) for i in range(1, level)),
                    start=0)
        return self.list[start:start + self.getMaxNodeCountByLevel(level)]


if __name__ == "__main__":
    # tests!
    assert ListBasedBinaryTree.getMaxNodeCountByLevel(
        1) == 1, "trees should have one node in their first level"
    assert ListBasedBinaryTree.getMaxNodeCountByLevel(
        2) == 2, "trees should have two nodes in their second level"
    assert ListBasedBinaryTree.getMaxNodeCountByLevel(
        3) == 4, "trees should have four nodes in their third level"

    test1 = ListBasedBinaryTree([1, 2, 3])
    assert test1.height == 2, "tree should have a height of 2"
    assert test1.getNodesByLevel(1) == [
        1
    ], "level 1 should have the first list item in it"
    assert test1.getNodesByLevel(2) == [
        2, 3
    ], "level 2 should have the second and third list items in it"

    print("tests passed")
