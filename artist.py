from tree import ListBasedBinaryTree
from svg import SVGElement

NODE_RADIUS = 20
NODE_DIAMETER = NODE_RADIUS * 2
MIN_NODE_X_SPACING = 5
NODE_TEXT_SIZE = 10
NODE_Y_SPACING = 8
# these need only affect the viewbox:
VERTICAL_MARGIN = 10
HORIZONTAL_MARGIN = 10


def visualizeBinaryTree(tree: ListBasedBinaryTree):
    """Produces an SVG that visualizes the tree. For simplicity, the root node is
    placed at the origin of the SVG's coordinate system and the viewBox is built
    around that."""
    finalHeight = tree.height * NODE_DIAMETER + (tree.height -
                                                 1) * NODE_Y_SPACING
    nodesInLastLevel = tree.getMaxNodeCountByLevel(tree.height)
    finalWidth = nodesInLastLevel * NODE_DIAMETER + (nodesInLastLevel -
                                                     1) * MIN_NODE_X_SPACING
    # SVG viewbox format is "minX minY width height"
    viewBox = (f"{(-finalWidth/2)-HORIZONTAL_MARGIN} " +
               f"{-NODE_RADIUS-VERTICAL_MARGIN} "
               f"{finalWidth + HORIZONTAL_MARGIN*2} " +
               f"{finalHeight + VERTICAL_MARGIN*2}")
    svgBase = SVGElement.getDefaultContainer(viewBox)
