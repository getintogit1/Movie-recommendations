import requests
import json
from tkinter import *
from customtkinter import *
import csv
from tksheet import Sheet
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

class DataBaseError(Exception):
    pass

TMDB_API_KEY = "bd9b6a447934f21e6dd53de84728bc9d"  

'''Here we want to give as parameter movies and want to recieve some recommendations,before
we need to specify the amount of recommendations by an int '''
def getRelatedMovies(num_related, *movie_titles):
    related_movies = []
    if num_related > 0:
    
        for title in movie_titles:
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
            response = requests.get(search_url)
            data = response.json()
            try:
                if response.status_code == 200 and data.get("results"):
                    movie_id = data["results"][0]["id"]
                    related_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US&page=1"
                    related_response = requests.get(related_url)
                    related_data = related_response.json()
                    if related_response.status_code < 400 and related_data.get("results"):
                        related_titles:list = [movie["title"] for movie in related_data["results"][:num_related]]  # get the first entries until the input limit
                        related_movies.extend(related_titles)
                    else:
                        raise ConnectionError(f"Error getting related movies for {title}")
                else:
                    raise DataBaseError(f"Error finding movie with title: {title}")
                
            except (DataBaseError, ConnectionError) as e:
                tk.messagebox.showinfo(f'Error', str(e))
    else:
        raise ValueError("Only amout greater than 0 is allowed")
    return related_movies

