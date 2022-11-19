import json
import pathlib
from json_store import JsonStore

film_path = pathlib.Path().resolve().parent / "storage/films.json"

class Film:

    def __init__(self, title):
        self.title = title
        self.creador = None
        self.firma = None


    def store_film(self):
        """
        Creates a new film dict, and stores it to the films.json
        :return:
        """
        # First, creates the review
        new_film = self.create_film_item()
        store = JsonStore(film_path)
        # Search if the user have previus reviews
        user_data = store.find_item("title", new_film)
        if user_data != None:
            print("Ya existe una película con ese título!")
            return
        else:
            store.addnew(new_film)
            return


    def create_film_item(self) -> dict:
        """
        Creates a new dictionary item with the film
        :return: the new dict
        """
        new_film = {"title": self.title, "creador": self.creador}
        """, "firma": self.firma"""
        return new_film