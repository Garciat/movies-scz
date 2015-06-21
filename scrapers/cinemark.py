from bs4 import BeautifulSoup
import requests
import json
from joblib import Parallel, delayed

def cinemark_scrape(cinema):
    r = requests.get('http://www.cinemark.com.bo/cines/' + cinema)
    soup = BeautifulSoup(r.text)
    
    films = []
    
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
            'movie_slug': movie_slug,
            'movie_url': movie_url,
            'title': title_text,
            'poster_url': poster_url,
            'performances': performances
        })
    
    imdb_results = Parallel(n_jobs = 4)(delayed(cinemark_movie_imdb)(film['movie_slug']) for film in films)
    
    for (film, imdb) in zip(films, imdb_results):
        film['imdb'] = imdb
    
    return films

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
