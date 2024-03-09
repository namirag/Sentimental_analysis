from monodb_.mongodb_collection import data_base_collection
from monodb_.todo_mongodb_collection import user_database_collection
from db_.db_common_method import dbMethods
from user_constructor import user_const
import traceback


class accessing_data(dbMethods):

    def calling_insert_method(self, user_data):
        dbc = data_base_collection()
        status = dbc.insert(imported_user_data=user_data)
        return status

    def calling_update_method(self, user_email, new_data):
        dbc = data_base_collection()
        data = dbc.update(imported_user_email=user_email, new_data=new_data)
        if data['status']:
            return True
        else:
            return False

    def calling_fetch_by_email_method(self, user_email):
        # global sen_user_email, sen_user_password
        global sen_user_email, sen_user_password
        try:
            dbc = data_base_collection()
            data = dbc.fetch_all_by_email(user_email)
            if data:
                for document in data:
                    sen_user_password = document['sen_user_password']
                    sen_user_email = document['sen_user_email']
                result = {True: [sen_user_email, sen_user_password]}
                return result
            else:
                return dict(False, 'data not found')
        except Exception as err:
            print(f"caught an {err} in data calling py file, fetch by email method.")

    def calling_user_note_insert(self, user_import):
        try:
            user_note_input = user_database_collection()
            status = user_note_input.insert(imported_user_data=user_import)
            return status if status else False
        except Exception as err:
            print(f"caught an {err} in data calling py file, fetch by email method.")

    # def calling_fetch_email(self, user_session_value):
    #     try:
    #         user_db_collection = user_database_collection()
    #
    #         email_ = user_db_collection.fetch_user_data(user_key_value=user_session_value)
    #         if email_['status'] == 'fail':
    #             return False
    #         else:
    #             return email_
    #     except Exception as err:
    #         print(f"caught an {err} in data calling py file, fetch by email method.")

    def calling_fetch_all_list(self, user_session_value):
        try:
            user_db_collection = user_database_collection()
            data = user_db_collection.fetch_user_data(user_key_value=user_session_value)
            # return data
            if data:
                return data
            else:
                return False
        except Exception as err:
            # traceback.print_exc()
            print(f"caught an -{err}- in data calling py file, fetch by email method.")
