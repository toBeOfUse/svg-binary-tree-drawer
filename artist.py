from tree import ListBasedBinaryTree
from svg import SVGElement

NODE_RADIUS = 20
NODE_DIAMETER = NODE_RADIUS * 2
MIN_NODE_X_SPACING = 15
NODE_TEXT_SIZE = 20
NODE_Y_SPACING = 8
NODE_OUTLINE_WIDTH = 3
# these need only affect the viewbox:
VERTICAL_MARGIN = 10
HORIZONTAL_MARGIN = 10


def visualizeBinaryTree(tree: ListBasedBinaryTree,
                        addBlankExternalNodes: bool = False):
    """Produces an SVG that visualizes the tree. For simplicity, the root node is
    placed at the origin of the SVG's coordinate system and the viewBox is built
    around that. If addBlankExternalNodes is True, then no existing nodes will be
    drawn external, but each of them will be given a placeholder external left and
    right child, if necessary."""
    numLevels = tree.height if not addBlankExternalNodes else tree.height + 1
    finalHeight = numLevels * NODE_DIAMETER + (numLevels - 1) * NODE_Y_SPACING
    nodesInLastLevel = tree.getMaxNodeCountByLevel(numLevels)
    # returns the distance between the left edge of the leftmost circle and the right
    # edge of the rightmost circle

    def getRowWidthByNodeCount(x): return x * NODE_DIAMETER + (
        x - 1) * MIN_NODE_X_SPACING
    finalWidth = getRowWidthByNodeCount(nodesInLastLevel)
    lowestCenterX = -finalWidth / 2 + NODE_RADIUS
    # SVG viewbox format is "minX minY width height"
    viewBox = (f"{(-finalWidth/2)-HORIZONTAL_MARGIN} " +
               f"{-NODE_RADIUS-VERTICAL_MARGIN} "
               f"{finalWidth + HORIZONTAL_MARGIN*2} " +
               f"{finalHeight + VERTICAL_MARGIN*2}")
    svgBase = SVGElement.getDefaultContainer(viewBox)

    prevSpacing = None
    prevYCenter = None
    # we build the tree from the bottom up so that we can space the bottom row of
    # nodes the minimum distance apart and then space each node in each row above it
    # halfway between their two child nodes.
    # if we are adding blank external nodes, we need an extra level (which will be
    # filled with Nones)
    for level in range(numLevels, 0, -1):
        nodes = tree.getNodesByLevel(level)
        nodes += [None] * (tree.getMaxNodeCountByLevel(level) - len(nodes))
        rowCenterY = (level - 1) * NODE_DIAMETER + (level - 1) * NODE_Y_SPACING
        rowWidth = finalWidth - (NODE_DIAMETER * (numLevels - level))
        nodeCentersSpan = rowWidth - NODE_DIAMETER
        if prevSpacing is None:
            nodeXSpacing = [0] + [
                nodeCentersSpan * (x / (len(nodes) - 1))
                for x in range(1,
                               len(nodes) - 1)
            ] + [nodeCentersSpan]
        else:
            nodeXSpacing = []
            for i in range(0, len(prevSpacing), 2):
                nodeXSpacing.append((prevSpacing[i] + prevSpacing[i + 1]) / 2)
        for i in range(len(nodes)):
            if nodes[i] is None:
                if not addBlankExternalNodes or not tree.hasParent(
                        level, i + 1):
                    continue

            nodeIsExternal = tree.isNodeExternal(level, i + 1)
            if addBlankExternalNodes:
                squareMode = nodes[i] is None
            else:
                squareMode = nodeIsExternal
            nodeCenterX = lowestCenterX + nodeXSpacing[i]
            # note that the tree class assumes that node numbers start at 1, whereas
            # in this loop we are coding with them starting at 0, so we have to add 1
            if not squareMode:
                svgBase.addChild(
                    SVGElement(
                        "circle", {
                            "cx": nodeCenterX,
                            "cy": rowCenterY,
                            "r": NODE_RADIUS,
                            "fill": "white",
                            "stroke": "black",
                            "stroke-width": NODE_OUTLINE_WIDTH
                        }))
            else:
                svgBase.addChild(
                    SVGElement(
                        "rect", {
                            "width": NODE_DIAMETER,
                            "height": NODE_DIAMETER,
                            "x": nodeCenterX - NODE_RADIUS,
                            "y": rowCenterY - NODE_RADIUS,
                            "fill": "white",
                            "stroke": "black",
                            "stroke-width": NODE_OUTLINE_WIDTH
                        }))
            if nodes[i] is not None:
                svgBase.addChild(
                    SVGElement(
                        "text", {
                            "x": nodeCenterX,
                            "y": rowCenterY,
                            "font-size": NODE_TEXT_SIZE,
                            "fill": "black",
                            "text-anchor": "middle",
                            "dominant-baseline": "middle",
                            "font-family": "sans-serif"
                        }, [nodes[i]]))
            if level != numLevels and tree.nodeExists(level, i + 1):
                if tree.hasLeftChild(level, i + 1) or addBlankExternalNodes:
                    leftChildXPos = lowestCenterX + prevSpacing[i * 2]
                    svgBase.addChild(
                        SVGElement(
                            "line", {
                                "x1": nodeCenterX,
                                "y1": rowCenterY,
                                "x2": leftChildXPos,
                                "y2": prevYCenter,
                                "stroke": "black",
                                "stroke-width": NODE_OUTLINE_WIDTH
                            }))
                if tree.hasRightChild(level, i + 1) or addBlankExternalNodes:
                    rightChildXPos = lowestCenterX + prevSpacing[i * 2 + 1]
                    svgBase.addChild(
                        SVGElement(
                            "line", {
                                "x1": nodeCenterX,
                                "y1": rowCenterY,
                                "x2": rightChildXPos,
                                "y2": prevYCenter,
                                "stroke": "black",
                                "stroke-width": NODE_OUTLINE_WIDTH
                            }))

        prevYCenter = rowCenterY
        prevSpacing = nodeXSpacing
    # sort the SVGElements so that the lines are first and thus are covered up by the shapes and things
    svgBase.children = [x for x in svgBase.children if x.tagName == "line"
                        ] + [x for x in svgBase.children if x.tagName != "line"]
    return svgBase


if __name__ == "__main__":
    testResult = visualizeBinaryTree(ListBasedBinaryTree(list(range(1, 7))),
                                     True)
    with open("test.svg", "w+") as testFile:
        testFile.write(testResult.render())
