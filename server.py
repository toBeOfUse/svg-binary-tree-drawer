import json
import tornado.ioloop
import tornado.web
from artist import visualizeBinaryTree
from tree import ListBasedBinaryTree


class SVGHandler(tornado.web.RequestHandler):

    def post(self):
        treeData = json.loads(self.request.body)
        print("got svg request:")
        print(treeData)
        elements = [(x.strip() if x.strip() != "" else None)
                    for x in treeData["elements"]]
        svgResult = visualizeBinaryTree(ListBasedBinaryTree(elements),
                                        treeData["squares"])
        self.finish("data:image/svg+xml;utf8," + svgResult.render())


if __name__ == "__main__":
    application = tornado.web.Application([(r"/svg", SVGHandler),
                                           (r"/(.*)",
                                            tornado.web.StaticFileHandler, {
                                                "path": "./static/",
                                                "default_filename": "index.html"
                                            })])
    application.listen(8888)
    print("listening on port 8888")
    tornado.ioloop.IOLoop.current().start()