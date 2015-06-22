# movies-scz

Incluir parametro `?callback=XYZ` para activar JSONP.

Formato de resultado en TypeScript por motivos descriptivos:

```typescript
class Result {
  movies: Movie[];
}

/*
 * Una película en cartelera.
 */
class Movie {
  id: string;
  movie_slug: string;
  movie_url: string;
  title: string;
  poster_url: string;
  imdb: ImdbDescription;
  performances: Performance[];
}

/*
 * Un horario de función de una película en cartelera.
 */
class Performance {
  type: string;
  date: string;
  time: string;
  timestamp: string; // ISO 8601
}

/*
 * Información de IMDB de la película.
 * Ver: http://www.omdbapi.com/
 */
class ImdbDescription { ... }
```

Ejemplo

```json
{
  "movies": [
    {
      "id": "732",
      "movie_slug": "732-la-noche-del-demonio-3",
      "movie_url": "http://www.cinemark.com.bo/cartelera/732-la-noche-del-demonio-3",
      "title": "La noche del demonio 3",
      "poster_url": "http://www.cinemark-bolivia.com/images/archivos/movies/732.jpg",
      "imdb": {
        "Type": "movie",
        "Language": "English",
        "Plot": "A prequel set before the haunting of the Lambert family that reveals how gifted psychic Elise Rainier reluctantly agrees to use her ability to contact the dead in order to help a teenage girl who has been targeted by a dangerous supernatural entity.",
        "Writer": "Leigh Whannell, Leigh Whannell (characters)",
        "Genre": "Horror",
        "Response": "True",
        "imdbID": "tt3195644",
        "Country": "USA",
        "Rated": "PG-13",
        "Director": "Leigh Whannell",
        "Year": "2015",
        "Actors": "Dermot Mulroney, Stefanie Scott, Angus Sampson, Leigh Whannell",
        "Released": "5 Jun 2015",
        "Runtime": "97 min",
        "Poster": "http://ia.media-imdb.com/images/M/MV5BMTUwNDU4NjE1N15BMl5BanBnXkFtZTgwOTc0MzA5NDE@._V1_SX300.jpg",
        "imdbRating": "N/A",
        "Metascore": "N/A",
        "imdbVotes": "N/A",
        "Title": "Insidious: Chapter 3",
        "Awards": "1 win."
      },
      "performances": [
        {
          "date": "21 Jun",
          "type": "DOB",
          "timestamp": "2015-06-21T20:00:00-04:00",
          "time": "20:00"
        },
        {
          "date": "22 Jun",
          "type": "DOB",
          "timestamp": "2015-06-22T20:00:00-04:00",
          "time": "20:00"
        },
        {
          "date": "23 Jun",
          "type": "DOB",
          "timestamp": "2015-06-23T20:00:00-04:00",
          "time": "20:00"
        },
        {
          "date": "24 Jun",
          "type": "DOB",
          "timestamp": "2015-06-24T19:30:00-04:00",
          "time": "19:30"
        }
      ]
    }
  ]
}
```
