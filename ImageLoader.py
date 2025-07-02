from PIL import Image, ImageTk
from io import BytesIO
import requests
from Utils import get_movie_data


class ImageLoader:


    def get_movie_images(self, movie_titles): #we get our movie title list from our search from cmdButtonClicked #1
        images = []
        for title in movie_titles:
            img = self.load_image(title) # in this fucntion we call our load image list 
            if img:
                images.append(img)
        print(type(images))
        return images
    
    def load_image(self, movie_title):
        data = get_movie_data(movie_title) # to load an image we need the data ( url) so we call our data function #2
        
        if 'Poster' in data:
            photo_url = data['Poster']
            response = requests.get(photo_url)
            img = Image.open(BytesIO(response.content))
            img = ImageTk.PhotoImage(img)
            #print(type(img))
            return img
        else:
            return None