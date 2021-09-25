from tree import ListBasedBinaryTree
from svg import SVGElement

NODE_RADIUS = 20
NODE_DIAMETER = NODE_RADIUS * 2
MIN_NODE_X_SPACING = 15
NODE_TEXT_SIZE = 10
NODE_Y_SPACING = 8
NODE_OUTLINE_WIDTH = 3
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
    # returns the distance between the left edge of the leftmost circle and the right
    # edge of the rightmost circle
    getRowWidthByNodeCount = lambda x: x * NODE_DIAMETER + (
        x - 1) * MIN_NODE_X_SPACING
    finalWidth = getRowWidthByNodeCount(nodesInLastLevel)
    # SVG viewbox format is "minX minY width height"
    viewBox = (f"{(-finalWidth/2)-HORIZONTAL_MARGIN} " +
               f"{-NODE_RADIUS-VERTICAL_MARGIN} "
               f"{finalWidth + HORIZONTAL_MARGIN*2} " +
               f"{finalHeight + VERTICAL_MARGIN*2}")
    svgBase = SVGElement.getDefaultContainer(viewBox)

    for level in range(1, tree.height + 1):
        nodes = tree.getNodesByLevel(level)
        nodeCenterYs = (level - 1) * NODE_DIAMETER + (level -
                                                      1) * NODE_Y_SPACING
        rowWidth = getRowWidthByNodeCount(len(nodes))
        nodeCentersSpan = rowWidth - NODE_DIAMETER
        nodeXSpacing = [0] + [
            nodeCentersSpan * (x / (len(nodes) - 1))
            for x in range(1,
                           len(nodes) - 1)
        ] + [nodeCentersSpan]
        lowestCenterX = -rowWidth / 2 + NODE_RADIUS
        print("row number is", level)
        print("row width is", rowWidth)
        print("node centers span", nodeCentersSpan)
        print("nodes are spaced out by", nodeXSpacing)
        print("lowestCenterX is", lowestCenterX)
        for i in range(len(nodes)):
            nodeCenterX = lowestCenterX + nodeXSpacing[i]
            svgBase.addChild(
                SVGElement(
                    "circle", {
                        "cx": nodeCenterX,
                        "cy": nodeCenterYs,
                        "r": NODE_RADIUS,
                        "fill": "white",
                        "stroke": "black",
                        "stroke-width": NODE_OUTLINE_WIDTH
                    }))
            svgBase.addChild(
                SVGElement(
                    "text", {
                        "x": nodeCenterX,
                        "y": nodeCenterYs,
                        "font-size": NODE_TEXT_SIZE,
                        "fill": "black"
                    }, [nodes[i]]))
    return svgBase


if __name__ == "__main__":
    testResult = visualizeBinaryTree(ListBasedBinaryTree([1, 2, 3]))
    with open("test.svg", "w+") as testFile:
        testFile.write(testResult.render())
