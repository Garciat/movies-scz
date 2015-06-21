import os
import tornado.ioloop
import tornado.web

from bs4 import BeautifulSoup
import requests
import json

def cinemark_scrape(cinema):
    r = requests.get('http://www.cinemark.com.bo/cines/' + cinema)
    soup = BeautifulSoup(r.text)

    films = []

    for movie_block in soup.select('.item2'):
        movie_id = movie_block.find_previous_sibling('a')['name']
        
        title_link = movie_block.select('.title3 > .red')[0]
        title_href = title_link['href']
        title_text = title_link.get_text()
        
        performances = []
        
        for day_block in movie_block.select('.tabbody'):
            day_date = day_block.find_previous_sibling('h4').get_text()
            
            for performance_block in day_block.find_all('div'):
                performance_type = performance_block.select('h5 > .red')[0].get_text()
                
                performance_time_string = performance_block.find('li').get_text()
                performance_times = list(map(lambda x: x.strip(), performance_time_string.split('|')))
                
                for performance_time in performance_times:
                    performances.append({
                        'type': performance_type,
                        'date': day_date,
                        'time': performance_time
                    })
        
        films.append({
            'id': movie_id,
            'title': title_text,
            'performances': performances
        })
    
    return films

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = cinemark_scrape('ventura-mall-santa-cruz')
        text = json.dumps(data, indent = 2, ensure_ascii = False).encode('utf8')
        
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.write(text)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()