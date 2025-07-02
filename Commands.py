from tkinter import *
from customtkinter import *
import csv
from tksheet import Sheet
import tkinter as tk
from MovieSearcher import MovieSearcher
from MovieRatings import MovieRater
from ImageLoader import ImageLoader


def reload(entry, amount, old_sheet, old_movie_frame, frame_results):
    """Destroy the old widgets and return brand-new ones."""
    # 1) destroy old sheet
    old_sheet.grid_forget()
    old_sheet.destroy()

    # 2) make new sheet
    new_sheet = Sheet(frame_results, page_up_down_select_row=True, column_width=120)
    new_sheet.grid(row=1, column=0, sticky="nswe")
    new_sheet.headers(['Movie Recommendation', 'Rating'])

    # 3) clear the entry fields
    amount.delete(0, 'end')
    entry.delete(0, 'end')

    # 4) destroy & recreate the movie_frame
    old_movie_frame.grid_forget()
    new_movie_frame = Frame(frame_results)
    new_movie_frame.grid(row=1, column=1, padx=10, pady=10)

    return new_sheet, new_movie_frame

def searchResults(entry, amount, sheet, frame_results, movie_frame):
    # --- parse & validate how many ---
    try:
        n = int(amount.get())
        if n < 1:
            raise ValueError
    except ValueError:
        tk.messagebox.showinfo("Error", "Please enter a positive integer.")
        return sheet, movie_frame

    # --- parse & validate titles ---
    titles = entry.get().split(', ')
    if not titles or any(not t for t in titles):
        tk.messagebox.showinfo("Error", "Enter at least one movie title.")
        return sheet, movie_frame
    if len(titles) > 3:
        tk.messagebox.showinfo("Error", "You can search up to 3 movies at once.")
        return sheet, movie_frame

    # Now that we’ve captured valid inputs, clear out the old UI:
    sheet, movie_frame = reload(entry, amount, sheet, movie_frame, frame_results)

    related = MovieSearcher().getRelatedMovies(n, *titles)
    ratings = MovieRater().getMovieRating(related)
    sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    images = ImageLoader().get_movie_images(titles)

    # display images
    for idx, img in enumerate(images, start=1):
        lbl = tk.Label(movie_frame, image=img)
        lbl.image = img
        lbl.grid(row=1, column=idx)

    # populate table
    for title, rating in sorted_ratings:
        sheet.insert_row([title, rating])

    # results header
    hdr = CTkLabel(frame_results, text=f"Results for: {', '.join(titles)}",
                   font=("Helvetica", 15))
    hdr.grid(row=0, column=0)

    return sheet, movie_frame
def downloadResults(sheet):
    if not sheet:
        tk.messagebox.showinfo("Error", "No data to download.")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )
    if not path:
        return  # user cancelled

    headers = sheet.headers()
    rows    = sheet.get_sheet_data()
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
