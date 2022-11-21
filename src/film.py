import json
import pathlib

import encrypt

from json_store import JsonStore
from encrypt import sign_message
from user import User

film_path = pathlib.Path().resolve().parent / "storage/films.json"


class Film:

    def __init__(self, title, creador: str):
        self.title = title
        self.creator_name = creador
        self.film_item = None
        self.create_film_item()


    def store_film(self):
        """
        Creates a new film dict, and stores it to the films.json
        :return:
        """
        # First, creates the review
        store = JsonStore(film_path)
        # Search if the user have previus reviews
        user_data = store.find_item("title", self.film_item)
        if user_data != None:
            print("Ya existe una película con ese título!")
            return
        else:
            store.addnew(self.film_item)
            return

    def create_film_item(self):
        """
        Creates a new dictionary item with the film
        :return: the new dict
        """
        self.film_item = {"title": self.title, "creador": self.creator_name}
        print(f"Generando film item: {self.film_item}")
        """, "firma": self.firma"""

    def sign_film(self, private_key: encrypt.RSAPrivateKey):
        """
        Signs the film and stores the signature on the signature member.
        We will be signing a stringified dictionary that holds the title and the username signing it.
        self.film_item = {creador: "authorname", title: "title"} -> sign(self.film_item) ->
        self.film_item = {creador: "authorname", title: "title", signatue: "signature"}
        """
        self.film_item["signature"] = encrypt.bytes_to_text(sign_message(
                                                        encrypt.text_to_bytes(str(self.film_item)),
                                                        private_key
                                                    ))

    @staticmethod
    def get_all_films() -> list:
        return JsonStore(film_path).load_data()