import os, sys
import tornado.ioloop
import tornado.web
import json

from datetime import timedelta

from utils import LazyTimedCache
from scrapers.cinemark import cinemark_scrape

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, cinemark_scz_data):
        self.cinemark_scz_data = cinemark_scz_data
    
    def get(self):
        jsonp = self.get_argument('callback', '')
        
        response = self.cinemark_scz_data.get()
        
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        
        if jsonp:
            self.write(jsonp + '(')
        
        self.write(response)
        
        if jsonp:
            self.write(')')

def cinemark_scz_data():
    def cinemark_scrape_scz():
        data = cinemark_scrape('ventura-mall-santa-cruz')
        result = { 'movies': data }
        return json.dumps(result, indent = 2, ensure_ascii = False).encode('utf8')
    
    return LazyTimedCache(cinemark_scrape_scz, timedelta(hours = 1))

application = tornado.web.Application([
    (r"/", MainHandler, dict(cinemark_scz_data = cinemark_scz_data())),
])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
