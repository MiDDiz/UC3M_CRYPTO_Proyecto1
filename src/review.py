import json
import pathlib
from json_store import JsonStore
import encrypt
import base64

#review_path = "D:/Universidad/3º Curso/Criptografia/Proyecto_final/storage/items.json"
review_path = pathlib.Path().resolve().parent / "storage/items.json"

class Review:
    def __init__(self, user):
        self.user = user

    def store_review(self, title: str, text: str, rating: str):
        """
        Creates a new review, and stores it to the input.txt
        :param title:
        :param text:
        :param rating:
        :return:
        """
        # First, creates the review
        new_rev = self.create_review_item(title, text, rating)
        store = JsonStore(review_path)
        # Search if the user have previus reviews
        user_data = store.find_item(self.user.username)
        if user_data != None:
            # If it have previus reviews, open the list of reviews
            # string to bytes
            encrypted_reviews = base64.decodebytes(user_data["reviews"].encode("utf-8"))
            init_vector = base64.decodebytes(user_data["iv"].encode("utf-8"))
            # [{"title": algo, "review":otro, "score":otra},{...},...]
            # We get the chunk above of data encrypted and we decrypt it into a str
            data_decripted = encrypt.decrypt_data(self.user.data_key, init_vector, encrypted_reviews)
            # Then the data is a string with the format of a list, where each item is separated with a comma. So we
            # parse that list.
            """
            user_reviews = str(data_decripted).split(",")
            """
            user_reviews = json.loads(str(data_decripted))
            print(f"Decrypted data: {user_reviews}")
            updated = False
            # Checks if has a review on the same film/show
            # Now for each item on the list
            for review in user_reviews:
                """
                # We transform that list item, that has the format of a dict,
                # in a dict so we can work with it as JSON info.
                review = json.loads(review)"""
                # If it has, updates that review

                if review["title"] == new_rev["title"]:
                    review["text"] = new_rev["text"]
                    review["rating"] = new_rev["rating"]
                    updated = True
            if not updated:
                # If is a new review, it appends it to the previous ones
                user_reviews.append(new_rev)
            (in_vector, user_reviews_encrypted) = encrypt.encrypt_data(self.user.data_key, base64.b64encode(str(user_reviews).encode("utf-8")))
            # Then, saves the new list of reviews instead of the old ones
            store.replace_item(user_data, self.update_reviews(user_reviews_encrypted, in_vector))
        else:
            # If user don't have previous reviews, it creates a new list of reviews
            user_reviews = []
            user_reviews.append(new_rev)
            # Encrypt user reviews
            (in_vector, user_reviews_encrypted) = encrypt.encrypt_data(self.user.data_key, base64.b64encode(str(user_reviews).encode("utf-8")))
            # Then creates a new entry in items with the user and his first review
            store.addnew(self.update_reviews(user_reviews_encrypted, in_vector))

    def create_review_item(self, title: str, text: str, rating: str) -> dict:
        """
        Creates a new dictionary item with the review
        :param title:
        :param text:
        :param rating:
        :return: the new dict
        """
        new_review = {"title": title, "text": text, "rating": rating}
        return new_review

    def update_reviews(self, user_reviews: bytes, input_vector: bytes) -> dict:
        """
        Creates a new dict that wlii be stored in items.json with
        the user, and a list of his reviews
        :param input_vector:
        :param user_reviews:
        :return:
        """
        new_user_review = {
            "username": self.user.username,
            "reviews": base64.b64encode(user_reviews).decode("utf-8"),
            "iv": (base64.b64encode(input_vector)).decode("utf-8")
        }
        return new_user_review
