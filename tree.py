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
    def height(self) -> int:
        return math.ceil(math.log2(len(self.list)))

    @staticmethod
    def getMaxNodeCountByLevel(level: int) -> int:
        return 2**(level - 1)

    @classmethod
    def getLevelStart(cls, level: int) -> int:
        """Returns the index of the first node that belongs to the given level. Meant
        to be used to index into self.list"""
        # can this be turned from log(n) into constant time ??
        return sum((cls.getMaxNodeCountByLevel(i) for i in range(1, level)),
                   start=0)

    def getNodesByLevel(self, level: int) -> list:
        start = self.getLevelStart(level)
        return self.list[start:start + self.getMaxNodeCountByLevel(level)]

    def nodeExistsByIndex(self, index: int) -> bool:
        """Checks for node existence by index, where index is used to look into
        self.list"""
        return index < len(self.list) and self.list[index] is not None

    def nodeExists(self, level: int, number: int) -> bool:
        """Checks for node existence by position. Both levels and node numbers are
        assumed to start at 1."""
        nodePos = self.getLevelStart(level) + (number - 1)
        return self.nodeExistsByIndex(nodePos)

    def hasLeftChild(self, level: int, number: int) -> bool:
        """Given the position of a node, returns whether it has a left child or not.
        Both levels and node numbers are assumed to start at 1."""
        nodePos = self.getLevelStart(level) + (number - 1)
        childPos = nodePos * 2 + 1
        return self.nodeExistsByIndex(childPos)

    def hasRightChild(self, level: int, number: int) -> bool:
        """Given the position of a node, returns whether it has a right child or not.
        Both levels and node numbers are assumed to start at 1."""
        nodePos = self.getLevelStart(level) + (number - 1)
        childPos = nodePos * 2 + 2
        return self.nodeExistsByIndex(childPos)

    def isNodeExternal(self, level: int, number: int) -> bool:
        """Given the position of a node, returns whether it has children or not. Both
        levels and node numbers are assumed to start at 1."""
        return (not self.hasLeftChild(
            level, number)) and (not self.hasRightChild(level, number))

    def hasParent(self, level: int, number: int) -> bool:
        """Given the position of a node which may or may not exist, returns whether
        it would have a parent if it did/does exist. Both levels and node numbers are
        assumed to start at 1."""
        nodePos = self.getLevelStart(level) + (number - 1)
        if nodePos < 1:
            return False
        else:
            parentPos = int((nodePos - 1) / 2)
            return self.nodeExistsByIndex(parentPos)


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
    assert not test1.isNodeExternal(1, 1), "root node is not external"
    assert test1.isNodeExternal(2, 1), "external node is external"
    #TODO: tests for left and right child existence

    print("tests passed")
