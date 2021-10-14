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
                        addBlankExternalNodes: bool = False,
                        makeBlankExternalNodesBlack: bool = True,
                        addWhiteBG: bool = False):
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

    # as we iterate over the horizontal rows of nodes, we store some data about the
    # previous row to help us out
    prevSpacing = None
    prevYCenter = None
    # this stores an array of boolean values describing whether each node from the
    # previous row was drawn or not. obviously, we initialize it to all False
    prevDrawnNodes = [False] * tree.getMaxNodeCountByLevel(numLevels+1)
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
        currentDrawnNodes = []
        for i in range(len(nodes)):
            leftChildWasDrawn = prevDrawnNodes[i*2]
            rightChildWasDrawn = prevDrawnNodes[i*2+1]
            # this might be different from Actually being external if we drew
            # placeholder blank children for this node
            effectivelyExternal = not (leftChildWasDrawn or rightChildWasDrawn)
            if nodes[i] is None:
                # we still draw blank nodes if we're adding blank external node
                # children or we need to add ghostly representations of parents that
                # "should" exist
                if effectivelyExternal:
                    # ^ if a node does have children, we should draw it
                    if not addBlankExternalNodes or (not tree.hasParent(level, i+1)):
                        # ^ if we're not drawing blank external nodes, or if the
                        # current node has no "real" node parents to draw blank
                        # children for, we skip this one
                        currentDrawnNodes.append(False)
                        continue
            currentDrawnNodes.append(True)
            squareMode = effectivelyExternal
            # blank nodes that Should exist because they have children will be
            # represented as dashed-line ghosts
            dashMode = {
                "stroke-dasharray": "4"} if (nodes[i] is None and not effectivelyExternal) else {}
            nodeCenterX = lowestCenterX + nodeXSpacing[i]
            # note that the tree class assumes that node numbers start at 1, whereas
            # in this loop we are coding with them starting at 0, so we have to add 1
            if nodes[i] is not None and nodes[i].startswith("$red"):
                shape_fill = "red"
                text_fill = "black"
                nodes[i] = nodes[i].replace("$red", "").strip()
            elif nodes[i] is not None and nodes[i].startswith("$black"):
                shape_fill = "black"
                text_fill = "white"
                nodes[i] = nodes[i].replace("$black", "").strip()
            else:
                shape_fill = "white"
                text_fill = "black"
            if not squareMode:
                svgBase.addChild(
                    SVGElement(
                        "circle", {
                            "cx": nodeCenterX,
                            "cy": rowCenterY,
                            "r": NODE_RADIUS,
                            "fill": shape_fill,
                            "stroke": "black",
                            "stroke-width": NODE_OUTLINE_WIDTH
                        } | dashMode))
            else:
                svgBase.addChild(
                    SVGElement(
                        "rect", {
                            "width": NODE_DIAMETER,
                            "height": NODE_DIAMETER,
                            "x": nodeCenterX - NODE_RADIUS,
                            "y": rowCenterY - NODE_RADIUS,
                            "fill": ("black"
                                     if (nodes[i] is None and makeBlankExternalNodesBlack)
                                     else shape_fill),
                            "stroke": "black",
                            "stroke-width": NODE_OUTLINE_WIDTH
                        } | dashMode))
            if nodes[i] is not None:
                svgBase.addChild(
                    SVGElement(
                        "text", {
                            "x": nodeCenterX,
                            "y": rowCenterY,
                            "font-size": NODE_TEXT_SIZE,
                            "fill": text_fill,
                            "text-anchor": "middle",
                            "dominant-baseline": "middle",
                            "font-family": "LiberationSans, sans-serif"
                        }, [nodes[i]]))
            if level != numLevels:
                if leftChildWasDrawn:
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
                            } | dashMode))
                if rightChildWasDrawn:
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
                            } | dashMode))

        prevYCenter = rowCenterY
        prevSpacing = nodeXSpacing
        prevDrawnNodes = currentDrawnNodes
    viewBoxComps = svgBase.attrs["viewBox"].split()
    bg = [
        SVGElement(
            "rect",
            {"fill": "white", "x": viewBoxComps[0],
             "y": viewBoxComps[1],
             "width": viewBoxComps[2],
             "height": viewBoxComps[3]})] if addWhiteBG else []
    # sort the SVGElements so that the lines are first and thus are covered up by the
    # shapes and things. also the background is even before them
    svgBase.children = bg + [x for x in svgBase.children if x.tagName == "line"
                             ] + [x for x in svgBase.children if x.tagName != "line"]
    return svgBase


if __name__ == "__main__":
    testResult = visualizeBinaryTree(ListBasedBinaryTree(list(range(1, 7))),
                                     True)
    with open("test.svg", "w+") as testFile:
        testFile.write(testResult.render())
