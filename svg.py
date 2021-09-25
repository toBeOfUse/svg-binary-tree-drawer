from typing import Union


class SVGElement:

    def __init__(self, tagName: str, attrs: dict = {}, children: list = []):
        self.tagName = tagName
        self.attrs = attrs
        self.children = children

    def setAttr(self, key: str, value: Union[str, int]):
        """Use this to set attributes on the SVG element like "height" or "fill". Set
        an attribute to an empty string to delete it."""
        if value != "":
            self.attrs[key] = str(value)
        elif key in self.attrs:
            del self.attrs[key]

    @classmethod
    def getDefaultContainer(cls,
                            viewBox: str = "0 0 100 100",
                            extraAttrs: dict = {},
                            initialChildren: list = []):
        return cls("svg", {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": viewBox
        } | extraAttrs, initialChildren)

    def addChild(self, child):
        self.children.append(child)

    def render(self, depth=0) -> str:
        tab = "    " * depth
        renderedChildren = "\n".join(c.render(depth + 1) for c in self.children)
        renderedAttrs = " ".join(k + f'="{v}"' for k, v in self.attrs.items())
        return tab + f"<{self.tagName} " + renderedAttrs + (
            "/>" if len(self.children) == 0 else
            (">\n" + renderedChildren + f"\n{tab}</{self.tagName}>"))


if __name__ == "__main__":
    test = SVGElement("circle", {"cx": 45, "cy": 45, "r": 40, "fill": "red"})
    print("circle:")
    print(test.render())
    testCont = SVGElement.getDefaultContainer()
    testCont.addChild(test)
    print("circle in container:")
    print(testCont.render())
    with open("test.svg", "w+", encoding="utf-8") as testFile:
        testFile.write(testCont.render())
