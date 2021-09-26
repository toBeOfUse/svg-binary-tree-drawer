import json
import tornado.ioloop
import tornado.web
from urllib import parse
import logging
from cairosvg import svg2png
from artist import visualizeBinaryTree
from tree import ListBasedBinaryTree


def treeDataToSVG(treeData: dict):
    elements = [(x.strip()[:10] if x.strip() != "" else None)
                for x in treeData["elements"]]
    svgResult = visualizeBinaryTree(ListBasedBinaryTree(elements),
                                    treeData["squares"])
    return svgResult


class SVGHandler(tornado.web.RequestHandler):

    def post(self):
        if len(self.request.body) > 500:
            self.set_status(400, "request too long")
            self.finish()
            logging.info("denied request for being "+str(len(self.request.body)+" bytes long"))
        else:
            treeData = json.loads(self.request.body)
            logging.info("got svg request:")
            logging.info(str(treeData))
            svg = treeDataToSVG(treeData)
            dataURL = "data:image/svg+xml," + parse.quote(svg.render())
            self.finish({"width": svg.viewBoxWidth, "url": dataURL})


class PNGHandler(tornado.web.RequestHandler):

    def post(self):
        if len(self.request.body) > 500:
            self.set_status(400)
            self.finish("request too long")
            logging.info("denied request for being "+str(len(self.request.body)+" bytes long"))
        else:
            logging.info("rendering png")
            treeData = json.loads(self.request.body)
            svg = treeDataToSVG(treeData)
            png = svg2png(bytestring=svg.render(), output_width=svg.viewBoxWidth*2)
            self.set_header("Content-Type", "image/png")
            self.finish(png)


if __name__ == "__main__":
    application = tornado.web.Application([(r"/svg", SVGHandler),
                                           (r"/png", PNGHandler),
                                           (r"/(.*)",
                                            tornado.web.StaticFileHandler, {
                                                "path": "./static/",
                                                "default_filename": "index.html"
                                            })],
                                          compress_response=True)
    application.listen(8888)
    print("listening on port 8888")
    logging.basicConfig(
        filename='requests.log', encoding='utf-8', level=logging.DEBUG,
        format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    tornado.ioloop.IOLoop.current().start()
