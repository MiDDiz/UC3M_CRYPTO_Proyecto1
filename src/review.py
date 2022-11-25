import json
import pathlib
from json_store import JsonStore
import encrypt
from encrypt import text_to_bytes, b64text_to_bytes, bytes_to_text
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
        user_data = store.find_item_usr(self.user.username)
        if user_data != None:
            self.overwrite_act_userdata(new_rev, store, user_data)
        else:
            self.write_new_userdata(new_rev, store)

    def write_new_userdata(self, new_rev, store):
        # If user don't have previous reviews, it creates a new list of reviews
        user_reviews = []
        user_reviews.append(new_rev)
        # Encrypt user reviews
        (in_vector, user_reviews_encrypted) = encrypt.encrypt_data(self.user.data_key,
                                                                   text_to_bytes(str(user_reviews)))
        # Then creates a new entry in items with the user and his first review
        store.addnew(self.update_reviews(user_reviews_encrypted, in_vector))

    def overwrite_act_userdata(self, new_rev, store, user_data):
        user_reviews = self.decode_actual_userdata(user_data)
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
        (in_vector, user_reviews_encrypted) = encrypt.encrypt_data(self.user.data_key,
                                                                   text_to_bytes(str(user_reviews)))
        # Then, saves the new list of reviews instead of the old ones
        store.replace_item(user_data, self.update_reviews(user_reviews_encrypted, in_vector))

    def decode_actual_userdata(self, user_data):
        # If it have previous reviews, open the list of reviews
        # string to bytes
        encrypted_reviews = b64text_to_bytes(user_data["reviews"])
        init_vector = b64text_to_bytes(user_data["iv"])
        # [{"title": algo, "review":otro, "score":otra},{...},...]
        # We get the chunk above of data encrypted and we decrypt it into a str
        data_decripted = encrypt.decrypt_data(self.user.data_key, init_vector, encrypted_reviews)
        # Then the data is a string with the format of a list, where each item is separated with a comma. So we
        # parse that list.
        """
                    user_reviews = str(data_decripted).split(",")
                    """
        data_decripted = base64.b64decode(data_decripted).decode("utf-8").replace("'", "\"")
        print(data_decripted)
        user_reviews = json.loads(str(data_decripted))
        print(f"Decrypted data: {user_reviews}")
        return user_reviews


    def find_user_reviews(self,username:str)->str:
        store = JsonStore(review_path)
        user_data = store.find_item_usr(username)
        return self.decode_actual_userdata(user_data)


    def find_single_review(self, username:str, title:str):
        user_reviews=self.find_user_reviews(username)
        for rev in user_reviews:
            if rev["title"] == title:
                return rev
        return None

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
            "reviews": bytes_to_text(user_reviews),
            "iv": bytes_to_text(input_vector)
        }
        return new_user_review
