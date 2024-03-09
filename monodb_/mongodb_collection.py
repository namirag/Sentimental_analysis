from pymongo import MongoClient
from db_.db_common_method import dbMethods
import html


class data_base_collection(dbMethods):

    # def __init__(self):
    #     self.collections = None
    #     self.db = None
    #     self.client = None

    def __init__(self):
        self.client = MongoClient(host='mongodb://localhost:27017/')
        self.db = self.client['sentimental_user']
        self.collections = self.db['user_collection']

    # data base creation
    def create(self):
        pass

    def insert(self, imported_user_data):
        try:
            client = MongoClient(host='mongodb://localhost:27017/')
            db = client['sentimental_user']
            collections = db['user_collection']
            user_data = {
                'user_first_name': imported_user_data.first_name[0],
                'user_last_name': imported_user_data.last_name[0],
                'user_birth_date': imported_user_data.birth_date[0],
                'user_gender': imported_user_data.gender[0],
                'sen_user_email': imported_user_data.sen_user_email[0][0],
                'sen_user_password': imported_user_data.sen_user_password
            }
            collections.insert_one(user_data)
            return {'status': True}

        except Exception as err:
            print(err)
            html.unescape(f"Caught an error &lth3&gt{err}&lt/h3&gt")
            return {'status': 'fails'}

    def update(self, imported_user_email, new_data):
        try:
            # Update a single document
            self.collections.update_one({"sen_user_email": imported_user_email}, {"$set": {"sen_user_password": new_data}})
            return {'status': True}
        except Exception as err:
            print(f"Caught an error in update - {err}")
            # html.unescape(f"Caught an error &lth3&gt{err}&lt/h3&gt")
            return {'status': 'fails'}

    def fetch_all_by_email(self, email):
        try:
            self.client = MongoClient(host='mongodb://localhost:27017/')
            self.db = self.client['sentimental_user']
            self.collections = self.db['user_collection']
            # Query documents with a specific condition
            data = self.collections.find({"sen_user_email": {"$eq": email}})
            return data
        except Exception as err:
            print(err)
            # html.unescape(f"Caught an error &lth3&gt{err}&lt/h3&gt")
            return {'status': 'fails'}

    def fetch_by_id(self, user_id):
        try:
            self.client = MongoClient(host='mongodb://localhost:27017/')
            self.db = self.client['sentimental_user']
            self.collections = self.db['user_collection']
            data = self.collections.find()
            return data
        except Exception as err:
            print(f"Caught an {err} in fetch by id function in mongodb file")

    def fetch_all(self):
        try:
            self.client = MongoClient(host='mongodb://localhost:27017/')
            self.db = self.client['sentimental_user']
            self.collections = self.db['user_collection']
            # Query all documents
            data = self.collections.find()
            if data:
                return data
            else:
                return {'status': 'fail'}
        except Exception as err:
            print(f"Caught an {err} in fetch all function in mongodb file")
            return {'status': 'fails'}

    def delete(self, imported_user_data):
        try:
            pass
        except Exception as err:
            html.unescape(f"Caught an error &lth3&gt{err}&lt/h3&gt")
            return {'status': 'fails'}
