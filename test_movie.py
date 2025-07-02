import unittest
import movie
from movie import DataBaseError
from unittest.mock import patch, Mock
from requests import get

from tkinter import *
from customtkinter import *

OMDB_API_KEY = '5ddf4335'

class MovieTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_getRelatedMovies(self):
        self.assertListEqual(movie.getRelatedMovies(2, ["The Matrix"]), ['The Matrix Reloaded', 'The Matrix Revolutions'])


    def test_getRelatedMovies_wrongTitle(self):
        self.assertEqual(movie.getRelatedMovies(2, "Python - The Movie!"),[])


    def test_getRelatedMovies_wrongAmount(self):
        with self.assertRaises(ValueError):
            movie.getRelatedMovies(-2, "Toy Story")


    def test_getMovieRating(self):
         self.assertEqual(movie.getMovieRating(["Toy Story"]), {'Toy Story': 100})


    def test_getMovieRating_NoIMDbRating(self):
         self.assertEqual(movie.getMovieRating(["Snow White and the Seven Dwarfs"]), {})


    @patch('movie.requests.get')
    def test_getMovieRating_mocked(self, mock_get):
        # Setup mock
        mock_response = Mock()
        response_ratings = {'DuckTyping': 75}
        mock_response.status_code = 200  # We assume the request is successful
        mock_response.json.return_value = response_ratings

        mock_get.return_value = mock_response

        result = movie.getMovieRating(["DuckTyping"])

        mock_get.assert_called_once_with(f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t=DuckTyping&r=json")  # Replace with the actual URL used in your function
        self.assertEqual(result, {})


    @patch('movie.requests.get')
    def test_getMovieRating_mocked_failed_request(self, mock_get):
        # mock
        mock_response = Mock()
        mock_response.status_code = 404  # we are not online
        mock_get.return_value = mock_response

        result = movie.getMovieRating(["Toy Story 2"])

        mock_get.assert_called_once_with("http://www.omdbapi.com/?apikey=5ddf4335&t=Toy Story 2&r=json") # Replace with the actual URL used in your function
        self.assertEqual(result,{})

    
    @patch("movie.filedialog.asksaveasfilename")
    @patch("movie.tk.messagebox.showinfo")
    def test_cmdDownload(self, mock_showinfo, mock_asksaveasfilename):
        # set mock
        mock_asksaveasfilename.return_value = "test_file.csv"
        mock_sheet = Mock()
        mock_sheet.headers.return_value = ["Column1", "Column2"]
        mock_sheet.get_sheet_data.return_value = [["Data1", "Data2"], ["Data3", "Data4"]]

        with patch("movie.sheet", mock_sheet):
            movie.cmdDownload()

        #actual assert tests
        mock_asksaveasfilename.assert_called_once_with(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        mock_showinfo.assert_not_called() 
        mock_sheet.headers.assert_called_once()
        mock_sheet.get_sheet_data.assert_called_once()

        expected_file_content = "Column1,Column2\nData1,Data2\nData3,Data4\n"
        with open("test_file.csv", "r") as file:
            file_content = file.read()
            self.assertEqual(file_content, expected_file_content)

    

if __name__ == "__main__":
    unittest.main()
