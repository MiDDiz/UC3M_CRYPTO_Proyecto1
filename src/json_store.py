import json


class JsonStore:
    def __init__(self, file_path):
        self.file_path=file_path


    def save_data(self, data:list[dict]):
        """
        Store a given data in a json file.
        It overwrites the new data on the file
        :param data:
        :return:
        """
        with open(self.file_path, "w", encoding="utf-8",newline="") as file:
            json.dump(data, file, indent=2)


    def load_data(self)->list[dict]:
        """
        returns a list with all the data that is found on a
        json file
        :return:
        """
        try:
            with open(self.file_path, "r", encoding="utf-8", newline="") as file:
                newdata=json.load(file)
        except:
            newdata=[]
        return newdata


    def find_item_usr(self, user:str):
        """
        finds if there is some data connected to the same user of the imput

        :param user:
        :return: Returns the found item if it finds one, or None if it don't
        """
        data = self.load_data()
        for item in data:
            if item["username"] == user:
                return item
        return None


    def addnew(self, item:dict):
        """
        store new items on the data
        :param item: item to be stored
        :return:
        """
        data = self.load_data()
        data.append(item)
        self.save_data(data)


    def replace_item(self, item, newitem):
        """
        replaces the item given with the newitem on the json
        :param item: item to be replaced
        :param newitem: item that replaces it
        :return:
        """
        data = self.load_data()
        data.remove(item)
        data.append(newitem)
        self.save_data(data)


    def find_item(self, field, newdata):
        """
        finds if there is some data connected to the same field of the imput
        :param field:
        :param data:
        :return:
        """
        data = self.load_data()
        for item in data:
            if item[field] == newdata:
                return item
        return None

    #TODO: de momento no se usa, si al final del proyecto sigue sin usarse, eliminarla
    def additem(self, item:dict):
        """
        add new items, and replace them in case they already exist
        :param item: item to be added/replaced
        :return:
        """
        found_item=self.find_item(item)
        if found_item==None:
            self.addnew(item)
        else:
            self.replace_item(found_item,item)

