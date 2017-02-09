#!/usr/bin/env python
import json
import os
import logging
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from instagram import photos_with_location
from settings import GOOGLE_TOKEN

define('environment', default='development', help='Pick you environment', type=str)
define('site_title', default='Tornado Example', help='Site Title', type=str)
define('cookie_secret', default='sooooooosecret', help='Your secret cookie dough', type=str)
define('port', default='8000', help='Listening port', type=str)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('main.html')


class FourOhFourHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.render('404.html')

    def post(self, *args, **kwargs):
        self.render('404.html')


class TagFormHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.render('map.html',
                    tag=self.get_argument('tag'),
                    count=self.get_argument('count'),
                    google_key=GOOGLE_TOKEN,
                    ws_url='ws{}://{}/websocket/'.format(
                        '' if '127.0.0.1' in self.request.host else 's',
                        self.request.host))


class WSHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        data = json.loads(message)
        for pic in photos_with_location(data['tag'], int(data['count'])):
            self.write_message(json.dumps(pic))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/map/', TagFormHandler),
            (r'/websocket/', WSHandler),
            (r'/([^/]+)', FourOhFourHandler),
        ]
        settings = dict(
            site_title=options.site_title,
            cookie_secret=options.cookie_secret,
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    print('http://127.0.0.1:' + str(options.port))
    logging.getLogger().setLevel(logging.DEBUG)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
