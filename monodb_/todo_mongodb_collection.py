from monodb_.mongodb_collection import data_base_collection
from pymongo import MongoClient
from db_.db_common_method import dbMethods
import datetime
import html


class user_database_collection(dbMethods):

    def __init__(self):
        self.client = MongoClient(host='mongodb://localhost:27017/')
        self.db = self.client['sentimental_user']
        self.collections = self.db['user_notes_collection']

    def insert(self, imported_user_data):
        try:
            client = MongoClient(host='mongodb://localhost:27017/')
            db = client['sentimental_user']
            collections = db['user_notes_collection']
            date = str(datetime.datetime.today())
            print(f"date - {date}")
            date = date.split(' ')[0]
            print(f"date - {date}")
            user_sentimental_data = {
                'user_sentimental_input': imported_user_data.user_note_input[0],
                'user_sentimental_emotion': imported_user_data.user_ai_emotion[0],
                'user_sentimental_data_date': date,
                'user_session_key': imported_user_data.user_session_key
            }
            collections.insert_one(user_sentimental_data)
            return True
        except Exception as err:
            print(f"Caught an {err} in fetch user data in file todo database collection")
            return False

    def fetch_user_email(self, user_key_value):
        try:
            client = MongoClient(host='mongodb://localhost:27017/')
            db = client['sentimental_user']
            collections = db['user_notes_collection']
            mon_collection = data_base_collection()
            data = mon_collection.fetch_all_by_email(email=user_key_value)
            for document in data:
                # taking only email
                user_email = document['sen_user_email']
                # print(user_email)
                if user_email:
                    return user_email
                else:
                    return {'status': 'fail'}
        except Exception as err:
            print(f"Caught an {err} in fetch user data in file todo database collection")

    def fetch_user_data(self, user_key_value):
        try:
            client = MongoClient(host='mongodb://localhost:27017/')
            db = client['sentimental_user']
            collections = db['user_notes_collection']
            data = collections.find({"user_session_key": {"$eq": user_key_value}})
            if data is not None:
                return data
            else:
                return False
        except Exception as err:
            print(f"Caught an {err} in fetch user data in file todo database collection")



