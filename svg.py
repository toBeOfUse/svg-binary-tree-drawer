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

    def render(self) -> str:
        return f"<{self.tagName} " + " ".join(
            k + f'="{v}"' for k, v in self.attrs.items()) + ">" + "\n".join(
                c.render() for c in self.children) + f"</{self.tagName}>"


if __name__ == "__main__":
    test = SVGElement("circle", {"rx": 45, "ry": 45, "r": 40, "fill": "red"})
    print("circle:")
    print(test.render())
    testCont = SVGElement.getDefaultContainer()
    testCont.addChild(test)
    print("circle in container:")
    print(testCont.render())
    with open("test.svg", "w+", encoding="utf-8") as testFile:
        testFile.write(testCont.render())
