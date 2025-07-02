import requests

OMDB_API_KEY = '5ddf4335' 
TMDB_API_KEY = "bd9b6a447934f21e6dd53de84728bc9d"  


def get_movie_data(title): #3
    search_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}&r=json"
    response = requests.get(search_url)
    data = response.json()
    everything_ok = response.status_code < 400 and data.get("Response") == "True"
    if everything_ok == False:  
        raise ConnectionError(f"Error finding movie with title: {title}")
    return data