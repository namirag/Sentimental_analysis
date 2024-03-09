import user_constructor as uc
from pathlib import Path


root_dir = Path.cwd()
sentimental_data = root_dir / 'data'

class constants:
    user_id = 'id'
    user_first_name = 'first_name'
    user_last_name = 'last_name'
    user_birth_date = 'birth_date'
    user_gender = 'gender'
    sen_user_email = 'sen_user_email'
    sen_user_password = 'sen_user_password'
    # user_sentimental_input = 'user_sentimental_input'
    # user_sentimental_emotion = 'user_sentimental_emotion'


