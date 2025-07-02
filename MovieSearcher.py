import DataBaseError
import requests
import tkinter as tk
from Utils import TMDB_API_KEY

TMDB_API_KEY = TMDB_API_KEY


class MovieSearcher:
    def getRelatedMovies(self, num_related:int , *movie_titles:str) -> list:
        related_movies = []
        if num_related >0:
            try:
                if num_related > 0:
                    for title in movie_titles:
                        movie_id = self.getMovieId(title)
                        related_titles = self.getRelatedTitles(movie_id, num_related)
                        related_movies.extend(related_titles)
            except (DataBaseError, ConnectionError) as e:
                tk.messagebox.showinfo(f'Error', str(e))
        else:
            raise ValueError("Only amout greater than 0 is allowed")
        return related_movies


    def getMovieId(self, title:str) ->int:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        response = requests.get(search_url)
        data = response.json()
        if response.status_code == 200 and data.get("results"):
            movie_id = data["results"][0]["id"]
        else: 
            raise ConnectionError(f"Error getting related movies for {title}")
        return movie_id


    def getRelatedTitles(self, movie_id:int, num_related:int) -> list:
        related_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US&page=1"
        related_response = requests.get(related_url)
        related_data = related_response.json()
        if related_response.status_code < 400 and related_data.get("results"):
            related_titles:list = [movie["title"] for movie in related_data["results"][:num_related]]  # get the first entries until the input limit
            print(related_titles)
            return related_titles
        else:
            raise DataBaseError(f"Error finding movies for movie id: {movie_id}")