import requests
import json
import re, locale
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
from joblib import Parallel, delayed

__bolivia_tz = timezone('America/La_Paz')
__months_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

def parse_date(s):
    ds, ms = s.split(' ')
    d = int(ds)
    m = __months_es.index(ms) + 1
    y = datetime.now().year
    return __bolivia_tz.localize(datetime(year = y, month = m, day = d))

def parse_time(s):
    hs, ms = s.split(':')
    h, m = int(hs), int(ms)
    return timedelta(hours = h, minutes = m)

def cinemark_scrape(cinema):
    r = requests.get('http://www.cinemark.com.bo/cines/' + cinema)
    soup = BeautifulSoup(r.text)
    
    movies = []
    
    for movie_block in soup.select('.item2'):
        movie_id = movie_block.find_previous_sibling('a')['name']
        
        title_link = movie_block.select('.title3 > .red')[0]
        title_href = title_link['href']
        title_text = title_link.get_text()
        
        movie_url = 'http://www.cinemark.com.bo' + title_href
        movie_slug = title_href.split('/')[-1]
        
        poster_img = movie_block.find('img')
        poster_url = poster_img['src']
        
        performances = []
        
        for day_block in movie_block.select('.tabbody'):
            day_date = day_block.find_previous_sibling('h4').get_text().strip()
            day_timestamp = parse_date(day_date)
            
            for performance_block in day_block.find_all('div'):
                performance_type = performance_block.select('h5 > .red')[0].get_text()
                
                performance_time_string = performance_block.find('li').get_text()
                performance_times = list(map(lambda x: x.strip(), performance_time_string.split('|')))
                
                for performance_time in performance_times:
                    performance_timestamp = day_timestamp + parse_time(performance_time)
                    
                    performances.append({
                        'type': performance_type,
                        'date': day_date,
                        'time': performance_time,
                        'timestamp': performance_timestamp.isoformat()
                    })
        
        movies.append({
            'id': movie_id,
            'movie_slug': movie_slug,
            'movie_url': movie_url,
            'title': title_text,
            'poster_url': poster_url,
            'performances': performances
        })
    
    imdb_results = Parallel(n_jobs = 4)(delayed(cinemark_movie_imdb)(m['movie_slug']) for m in movies)
    
    for (movie, imdb) in zip(movies, imdb_results):
        movie['imdb'] = imdb
    
    return movies

def cinemark_movie_imdb(movie_slug):
    r = requests.get('http://www.cinemark.com.bo/cartelera/' + movie_slug)
    soup = BeautifulSoup(r.text)
    
    original_title = soup.select('.movie-details > span.red')[0].next_sibling.strip()
    
    r = requests.get('http://www.omdbapi.com/', params = dict(t = original_title))
    imdb = json.loads(r.text)
    
    if imdb['Response'] == 'True':
        return imdb
    else:
        return None
