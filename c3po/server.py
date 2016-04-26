'''
Run this server

from c3po import Server
app = Server()
conf = Conf()
conf.import_type = 'path'
conf.client_module_path = '/xx/xx'
conf.client_module_name = 'hello'
app.register(conf)
app.run()
'''

import tornado.ioloop
import tornado.web

from handler import ServiceHandler, HelloHandler


class Stub(object):
    name = ''
    client_import_type = 'module'
    client_module = ''
    client_module_path = ''
    client_module_name = ''
    get_client_func = ''

    server_pb2_import_type = 'module'
    server_pb2_module = ''
    server_pb2_module_path = ''
    server_pb2_module_name = ''


class Server(object):
    stubs = dict()

    def __init__(self, host='0.0.0.0', port=8888, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    def register(self, stub):
        self.stubs[stub.name] = stub

    def run(self, debug=False):
        app = tornado.web.Application([
            ('/service/([^/]+)/call/([^/]+)',
             ServiceHandler, dict(stubs=self.stubs, debug=debug)),
            ('/',
             HelloHandler, dict(stubs=self.stubs, debug=debug))
        ], debug=debug)

        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()
