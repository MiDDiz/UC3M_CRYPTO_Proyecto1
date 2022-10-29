from json_store import JsonStore

review_path="D:/Universidad/3º Curso/Criptografia/Proyecto_final/storage/users.json"

class Review:
    def __init__(self, user):
        self.user=user

    def store_review(self, title:str, text:str, rating:str):
        """
        Creates a new review, and stores it to the input.txt
        :param title:
        :param text:
        :param rating:
        :return:
        """
        #First, creates the review
        new_rev=self.create_review_item(title,text,rating)
        store=JsonStore(review_path)
        #Search if the user have previus reviews
        user_data=store.find_item(self.user)
        if user_data!=None:
            # If it have previus reviews, open the list of reviews
            user_reviews=user_data["reviews"]
            updated=False
            #Checks if has a review on the same film/show
            for review in user_reviews:
                #If it has, updates that review
                if review["title"]==new_rev["title"]:
                    review["text"]=new_rev["text"]
                    review["rating"] = new_rev["rating"]
                    updated=True
            if not updated:
                #If is a new review, it appends it to the previous ones
                user_reviews.append(new_rev)
            #Then, saves the new list of reviews instead of the old ones
            store.replace_item(user_data,self.update_reviews(user_reviews))
        else:
            #If user don't have previous reviews, it creates a new list of reviews
            user_reviews=[]
            user_reviews.append(new_rev)
            #Then creates a new entry in items with the user and his first review
            store.addnew(self.update_reviews(user_reviews))




    def create_review_item(self, title:str, text:str, rating:str)->dict:
        """
        Creates a new dictionary item with the review
        :param title:
        :param text:
        :param rating:
        :return: the new dict
        """
        new_review={"title":title,"text":text,"rating":rating}
        return new_review

    def update_reviews(self,user_reviews:list[dict])->dict:
        """
        Creates a new dict that wlii be stored in items.json with
        the user, and a list of his reviews
        :param user_reviews:
        :return:
        """
        new_user_review={"usuario":self.user, "reivews":user_reviews}
        return new_user_review