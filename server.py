import json
import tornado.ioloop
import tornado.web
from cairosvg import svg2png
from artist import visualizeBinaryTree
from tree import ListBasedBinaryTree


def treeDataToSVG(treeData: dict):
    elements = [(x.strip()[:20] if x.strip() != "" else None)
                for x in treeData["elements"]]
    svgResult = visualizeBinaryTree(ListBasedBinaryTree(elements),
                                    treeData["squares"])
    return svgResult.render()


class SVGHandler(tornado.web.RequestHandler):

    def post(self):
        if len(self.request.body) > 500:
            self.set_status(400, "request too long")
            self.finish()
        else:
            treeData = json.loads(self.request.body)
            print("got svg request:")
            print(treeData)
            self.finish("data:image/svg+xml;utf8," + treeDataToSVG(treeData))


class PNGHandler(tornado.web.RequestHandler):

    def post(self):
        if len(self.request.body) > 500:
            self.set_status(400)
            self.finish("request too long")
        else:
            treeData = json.loads(self.request.body)
            svg = treeDataToSVG(treeData)
            png = svg2png(bytestring=svg, output_width=800)
            self.set_header("Content-Type", "image/png")
            self.finish(png)


if __name__ == "__main__":
    application = tornado.web.Application([(r"/svg", SVGHandler),
                                           (r"/png", PNGHandler),
                                           (r"/(.*)",
                                            tornado.web.StaticFileHandler, {
                                                "path": "./static/",
                                                "default_filename": "index.html"
                                            })])
    application.listen(8888)
    print("listening on port 8888")
    tornado.ioloop.IOLoop.current().start()
