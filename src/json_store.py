import json


class JsonStore:
    def __init__(self, file_path):
        self.file_path=file_path

    """The method save_data is used to store a given data in a json file.
    It overwrites the new data on the file"""
    def save_data(self, data:list[dict], type:str):
        path= self.file_path+type+".json"
        with open(path, "w", encoding="utf-8",newline="") as file:
            json.dump(data, file, indent=2)

    """This method returns a list with all the data that is found on a 
    json file"""
    def load_data(self,type:str)->list[dict]:
        path = self.file_path + type + ".json"
        try:
            with open(path, "r", encoding="utf-8", newline="") as file:
                newdata=json.load(file)
        except:
            newdata=[]
        return newdata

    """The method finds if there is some data connected to the same user
    as the new data"""
    def find_item(self, new_item, type):
        data = self.load_data(type)
        for item in data:
            if item["usuario"] == new_item["usuario"]:
                return item
        return None

    """addnew is only used to store new items on the data"""
    def addnew(self, item:dict, type:str):
        data = self.load_data(type)
        data.append(item)
        self.save_data(data, type)

    """replace_items replaces the item given with the newitem on the json """
    def replace_item(self, item, newitem, type):
        data = self.load_data(type)
        data.remove(item)
        data.append(newitem)
        self.save_data(data, type)

    """additem is used to add new items, and replace them in case they already exist"""
    def additem(self, item:dict, type:str):
        found_item=self.find_item(item,type)
        if found_item==None:
            self.addnew(item,type)
        else:
            self.replace_item(found_item,item,type)