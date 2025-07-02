import requests
import tkinter as tk
from Utils import OMDB_API_KEY, get_movie_data

OMDB_API_KEY = OMDB_API_KEY 

class MovieRater:
    def getMovieRating(self, movie_titles) -> dict:
        print(movie_titles, "From Movie Rater")
        ratings_dict = {}
        for title in movie_titles:
            try:
                rating = self.searchForRating(title)
                ratings_dict[title] = rating  # fill our output dict with score for title
                    

            except(ConnectionError, ValueError) as e:
                tk.messagebox.showinfo(f"Error" , str(e))
        return ratings_dict

    def searchForRating(self, title:str):
        data = get_movie_data(title)
        if "Ratings" in data:
            for rating_info in data["Ratings"]:
                if rating_info["Source"] == "Rotten Tomatoes":
                    rating = int(rating_info["Value"].strip('%'))
                    return rating
            else:
                raise ValueError(f"Rotten Tomatoes rating not found for {title}")
        else:
            raise ValueError(f"No rating information available for {title}")