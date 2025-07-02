import tkinter
import customtkinter
from typing import Optional
import PIL
from tkinter import *
from customtkinter import *
import tksheet
from tksheet import *
import tkinter as tk
from PIL import Image, ImageTk


#vars
TMDB_API_KEY: str
OMDB_API_KEY: str
image_list = list[PIL.ImageTk.PhotoImage]

#funcs
def getRelatedMovies(num_related: int, movie_titles: list) -> list:
    ...

def getMovieRating(movie_titles: list) -> dict:
    ...

def cmdDownload()-> None:
    ...

def reload()-> None:
    ...

def get_movie_data(title: str) -> dict:
    ...

def load_image(movie_title: str) -> Optional[PIL.ImageTk.PhotoImage]:
    ...

def get_movie_images(movie_titles: list) -> image_list:
    ...

def cmdSearch_button_clicked():
    ...

def cmdReload() -> None:
    ...

# CTk:
root: customtkinter.windows.ctk_tk.CTk
frame_results: tkinter.Frame
frame_search: tkinter.Frame
movie_frame: tkinter.Frame
amount_help: customtkinter.windows.widgets.ctk_label.CTkLabel
entry_help: customtkinter.windows.widgets.ctk_label.CTkLabel
download_btn: customtkinter.windows.widgets.ctk_button.CTkButton
reloaod_btn: customtkinter.windows.widgets.ctk_button.CTkButton
search_btn: customtkinter.windows.widgets.ctk_button.CTkButton
amount: customtkinter.windows.widgets.ctk_entry.CTkEntry
entry: customtkinter.windows.widgets.ctk_entry.CTkEntry
sheet: tksheet._tksheet.Sheet
