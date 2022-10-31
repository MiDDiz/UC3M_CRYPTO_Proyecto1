import pathlib

from json_store import JsonStore
import re
import encrypt

# user_path = "D:/Universidad/3º Curso/Criptografia/Proyecto_final/storage/users.json"
user_path = pathlib.Path().resolve().parent / "storage/users.json"

class User:

    def __init__(self):
        self.username = None
        self.data_key = None

    @staticmethod
    def password_parser(passwd: str) -> bool:
        """
        Checks if password is strong enough.
        :param passwd: password introduced by user.
        :return: true if secure enough.
        """

        with open('../storage/common_passwd.txt') as file:
            contents = file.read()
            if passwd in contents:
                return False
            print(passwd)
        pattern = re.compile("^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$")
        if not pattern.match(passwd):
            return False
        return True

    @classmethod
    def store_user(cls, usurname, passw) -> bool:
        """
        Search if a user exists, if it does not, it creates a new user,
        if it exists, checks if the password is correct
        :param usurname:
        :param passw:
        :return: True if the iser is new or the user exists and the password
        is correct, false if the password is not correct
        """
        store = JsonStore(user_path)
        new_user = cls.create_user_item(usurname, passw)
        found = store.find_item(new_user["username"])
        if (found == None):
            print("Creando nuevo usuario!")
            store.addnew(new_user)
            return True

        eq_passw = cls.compare_passw(found, new_user)
        return eq_passw

    @staticmethod
    def create_user_item(usurname: str, passw: str) -> dict:
        """
        Creates a new user that can be stored at a json
        :param usurname:
        :param passw:
        :return: A dictionary that the .json will store
        """
        newsalt= encrypt.generate_salt()
        user_item = {"username": usurname, "password": passw, "salt":newsalt}
        return user_item

    def compare_passw(self, item1: dict, item2: dict) -> bool:
        """
        Compares the password field from two dictionaries
        :param item1: first dict
        :param item2: second dict
        :return: True if passwords are the same, False in other case
        """
        if (item1["password"] == item2["password"]):
            return True
        else:
            return False

    @staticmethod
    def user_exists(user:str):
        store=JsonStore(user_path)
        return store.find_item(user)
