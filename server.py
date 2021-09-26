import json
from typing import Union
from svg import SVGElement
import tornado.ioloop
import tornado.web
from urllib import parse
import logging
from cairosvg import svg2png
from artist import visualizeBinaryTree
from tree import ListBasedBinaryTree


class ElementsHandler(tornado.web.RequestHandler):
    def requestToSVG(self) -> Union[SVGElement, None]:
        if len(self.request.body) > 500:
            self.set_status(400, "request too long")
            self.finish()
            logging.debug("denied request for being "+str(len(self.request.body))+" bytes long")
            return None
        try:
            treeData = json.loads(self.request.body)
        except:
            self.set_status(400, "invalid JSON")
            self.finish()
            logging.debug("denied request for being invalid JSON")
            return None
        if "elements" not in treeData or type(
                treeData["elements"]) is not list or "squares" not in treeData or type(
                treeData["squares"]) is not bool:
            self.set_status(400, "malformed request")
            self.finish()
            logging.debug("denied request for having malformed input: "+str(treeData))
            return None
        elements = [(x.strip()[:10] if x.strip() != "" else None)
                    for x in treeData["elements"]]
        svgResult = visualizeBinaryTree(ListBasedBinaryTree(elements),
                                        treeData["squares"])
        logging.info("processed request for tree: "+str(treeData))
        return svgResult


class SVGHandler(ElementsHandler):

    def post(self):
        svg = super().requestToSVG()
        if svg is not None:
            dataURL = "data:image/svg+xml," + parse.quote(svg.render())
            self.set_header("Content-Type", "application/json")
            self.finish({"width": svg.viewBoxWidth, "url": dataURL})


class PNGHandler(ElementsHandler):

    def post(self):
        svg = super().requestToSVG()
        if svg is not None:
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
