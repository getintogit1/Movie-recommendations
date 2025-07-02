import customtkinter as ctk
import tkinter as tk
from tksheet import Sheet
import Commands

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Movie Recommender")
        self.geometry("800x600")

        ctk.CTkLabel(self, text="Movies").grid(row=0, column=0, padx=10, pady=10)
        self.moviesEntry = ctk.CTkEntry(self, placeholder_text="Enter comma-separated titles")
        self.moviesEntry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=10)

        ctk.CTkLabel(self, text="Amount").grid(row=1, column=0, padx=10, pady=10)
        self.amountEntry = ctk.CTkEntry(self, placeholder_text="# of recommendations")
        self.amountEntry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=10)

        ctk.CTkButton(self, text="Search",   command=self.cmdSearch).grid(row=2, column=1, padx=10, pady=10)
        ctk.CTkButton(self, text="Download", command=self.cmdDownload).grid(row=2, column=2, padx=10, pady=10)

        self.frame_results = tk.Frame(self)
        self.frame_results.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        self.frame_results.rowconfigure(1, weight=1)
        self.frame_results.columnconfigure(0, weight=1)

        self.sheet = Sheet(
            self.frame_results,
            page_up_down_select_row=True,
            column_width=120
        )
        self.sheet.grid(row=1, column=0, sticky="nsew")
        self.movie_frame = tk.Frame(self.frame_results)
        self.movie_frame.grid(row=1, column=1, padx=10, pady=10)

        # make everything expand on resize
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def cmdSearch(self):
        self.sheet, self.movie_frame = Commands.searchResults(
            self.moviesEntry,
            self.amountEntry,
            self.sheet,
            self.frame_results,
            self.movie_frame
        )

    def cmdDownload(self):
        Commands.downloadResults(self.sheet)

if __name__ == "__main__":
    app = App()
    app.mainloop()
