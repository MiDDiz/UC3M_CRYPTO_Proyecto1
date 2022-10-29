import json


class JsonStore:
    def __init__(self, file_path):
        self.file_path=file_path

    """The method save_data is used to store a given data in a json file.
    It overwrites the new data on the file"""
    def save_data(self, data:list[dict]):
        with open(self.file_path, "w", encoding="utf-8",newline="") as file:
            json.dump(data, file, indent=2)

    """This method returns a list with all the data that is found on a 
    json file"""
    def load_data(self)->list[dict]:

        try:
            with open(self.file_path, "r", encoding="utf-8", newline="") as file:
                newdata=json.load(file)
        except:
            newdata=[]
        return newdata

    """The method finds if there is some data connected to the same user
    as the new data"""
    def find_item(self, new_item):
        data = self.load_data()
        for item in data:
            if item["usuario"] == new_item["usuario"]:
                return item
        return None

    """addnew is only used to store new items on the data"""
    def addnew(self, item:dict):
        data = self.load_data()
        data.append(item)
        self.save_data(data)

    """replace_items replaces the item given with the newitem on the json """
    def replace_item(self, item, newitem):
        data = self.load_data()
        data.remove(item)
        data.append(newitem)
        self.save_data(data)

    """additem is used to add new items, and replace them in case they already exist"""
    def additem(self, item:dict):
        found_item=self.find_item(item)
        if found_item==None:
            self.addnew(item)
        else:
            self.replace_item(found_item,item)