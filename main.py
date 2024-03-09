import html
from datetime import datetime

from flask import Flask, render_template, request, url_for, flash, session

import constant
from constant import constants as const
from user_constructor import user_const as usconst
from user_data_constructor import user_note_constructor as note_const
from db_.data_calling import accessing_data
import common_methods as co_methods
import os
import openai
import string
from flask_bcrypt import Bcrypt
import traceback
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "sentimental_user_key"

openai.api_key = os.getenv("OPEN_API_KEY")


@app.route("/sign_up", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        data = user_registration()
        if data is not False:
            return render_template(
                "login_page.html",
                email=data.sen_user_email,
                password=data.sen_user_password,
            )
        else:
            return render_template(
                "user_registration.html", status="here status of registration is shown"
            )
    else:
        return render_template(
            "user_registration.html", status="here status of registration is shown"
        )


def user_registration():
    ad = accessing_data()
    const.user_first_name = request.form["first_name"]
    const.user_last_name = request.form["last_name"]
    const.user_birth_date = request.form["date_of_birth"]
    const.user_gender = request.form["gender"]
    const.sen_user_email = request.form["email"]
    const.sen_user_password = request.form["password"]
    email_dict = co_methods.validating_email(const.sen_user_email)
    email_status = list(email_dict.keys())[0]
    email = list(email_dict.values())

    password_status = co_methods.validating_password(const.sen_user_password)
    if email_status and password_status:
        hashed_pass = const.sen_user_password
        encrypt_password = encrypt_pass(hashed_pass)
        user_en_data = usconst(
            const.user_first_name,
            const.user_last_name,
            const.user_birth_date,
            const.user_gender,
            sen_email=email,
            sen_password=encrypt_password,
        )
        status = ad.calling_insert_method(user_data=user_en_data)
        if status["status"] is True:
            return user_en_data  # , email, password
    else:
        return False


def encrypt_pass(entered_password):
    bcrypt = Bcrypt()
    hashed_pass = bcrypt.generate_password_hash(entered_password).decode("utf-8")
    return hashed_pass


def check_encrypt_pass(user_password, hashed_pass):
    bcrypt = Bcrypt()
    is_valid = bcrypt.check_password_hash(hashed_pass, user_password)
    return is_valid


@app.route("/login_page", methods=["POST", "GET"])
def login():
    try:
        if request.method == "POST":
            user_email = (request.form["email"]).lower()
            user_password = request.form["password"]

            if user_password == "" and user_email == "":
                return render_template(
                    "login_page.html", error_msg="please enter your data!!!"
                )
            else:
                ad = accessing_data()
                get_data = ad.calling_fetch_by_email_method(user_email=user_email)
                user_email_db = (list(get_data.values()))[0][0]
                user_password_db = (list(get_data.values()))[0][1]
                user_pass_status = check_encrypt_pass(user_password, user_password_db)
                if list(get_data.keys())[0]:
                    if user_email == user_email_db:
                        if user_pass_status:
                            session["email"] = user_email
                            return render_template("index.html")
                        else:
                            return render_template(
                                "login_page.html",
                                error_msg="entered password is not valid!",
                            )
                    else:
                        return render_template(
                            "login_page.html", error_msg="entered email is not valid!"
                        )
                else:
                    return render_template(
                        "login_page.html",
                        error_msg="you are not registered,\n please register yourself first!!!",
                    )
        else:
            return render_template(
                "login_page.html", error_msg="please enter your details"
            )

    except Exception as err:
        print(f"Caught an {err} in main file, login function")
        return render_template(
            "login_page.html", error_msg=html.unescape(f"you got error - {err}")
        )


@app.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    try:
        if request.method == "POST":
            user_email = (request.form["email"]).lower()
            user_password = request.form["password"]
            password_status = co_methods.validating_password(const.sen_user_password)
            hashed_pass = const.sen_user_password
            encrypt_password = encrypt_pass(hashed_pass)

            # Define password_status, hashed_pass, and encrypt_password here

            if user_password == "" and user_email == "":
                return render_template(
                    "forgot.html", error_msg="Please enter your data!!!"
                )
            else:
                ad = accessing_data()
                data_change_status = ad.calling_update_method(
                    user_email=user_email, new_data=encrypt_password
                )
                get_data = ad.calling_fetch_by_email_method(user_email=user_email)
                user_email_db = (list(get_data.values()))[0][0]
                if user_email == user_email_db:
                    if password_status:
                        if data_change_status:
                            return render_template("login_page.html")
                        else:
                            return render_template(
                                "forgot.html", error_msg="password not change"
                            )
                else:
                    return render_template(
                        "forgot.html", error_msg="email is not valid"
                    )
            return render_template("forgot.html", error_msg="please enter your details")
        # Define password validation and database update logic here
        else:
            return render_template("forgot.html", error_msg="Please enter your details")
    except Exception as err:
        print(f"Caught an {err} in main file, {traceback.print_exc()}")
        return render_template("forgot.html", error_msg=f"You got an error - {err}")


@app.route("/index", methods=["POST", "GET"])
def index():
    try:
        if request.method == "POST":
            email = session.get("email")
            sentimental_list = []
            if email:
                ad = accessing_data()
                user_sentimental_input = request.form["inputSentence"]  # hello2
                # user_ai_emotion = request.form['ai_emotion']
                user_login_credentials = ad.calling_fetch_by_email_method(
                    user_email=email
                )
                user_login_credentials_status = list(user_login_credentials.keys())[0]
                credential_list = list(user_login_credentials.values())[0]
                user_email = credential_list[0]
                user_pass = credential_list[1]
                if user_email == email:
                    if (
                        user_sentimental_input is not None
                        or user_sentimental_input != ""
                    ):
                        ai_emotion = openai_result_emotion(user_sentimental_input)
                        user_analysed_data = note_const(
                            user_note_input=user_sentimental_input,
                            user_ai_emotion=ai_emotion,  # 'no ai emotion',
                            user_session_key=email,
                        )
                        status = ad.calling_user_note_insert(
                            user_import=user_analysed_data
                        )
                        if status:
                            # call list of user added in database
                            user_sentimental_list = ad.calling_fetch_all_list(
                                user_session_value=email
                            )
                            print(user_sentimental_list)
                            # print(d.next())
                            user_sentimental_list = list(user_sentimental_list)
                            # print(f"user_sentimental_list - {user_sentimental_list}")
                            if user_sentimental_list:
                                for item in user_sentimental_list:
                                    sentimental_list.append(
                                        {
                                            "user_sentimental_input": item[
                                                "user_sentimental_input"
                                            ],
                                            "user_sentimental_emotion": item[
                                                "user_sentimental_emotion"
                                            ],
                                            "user_sentimental_data_date": item[
                                                "user_sentimental_data_date"
                                            ],
                                        }
                                    )
                                sentimental_df = pd.DataFrame(sentimental_list)
                                print(f"sentimental_df - {sentimental_df}")
                                file_path = constant.sentimental_data
                                date_to = str(datetime.today())
                                date = date_to.split(" ")[0]
                                sentimental_df.to_csv(
                                    file_path / f"{date}.csv", index=False
                                )
                                print(
                                    (pd.read_csv(file_path / f"{date}.csv")).to_string()
                                )
                                return render_template(
                                    "index.html",
                                    status=status,
                                    entries=user_sentimental_list,
                                )
                            else:
                                return render_template(
                                    "index.html", status="data is not inserted"
                                )
                    else:
                        return render_template(
                            "index.html", status="please enter data in input field"
                        )
                else:
                    return render_template("index.html", status="email not matched")
            else:
                return render_template(
                    "index.html", status="session is not created for this email"
                )
        else:
            # fetch all list here for show list button
            # ad = accessing_data()
            # email = session.get('email')
            # user_sentimental_list = ad.calling_fetch_all_list(user_session_value=email)
            # return render_template('index.html', entries=user_sentimental_list)
            return render_template("index.html")
    except Exception as err:
        print(f"Caught an {err} in main file, login function")
        return render_template(
            "index.html", status=html.unescape(f"you got error - {err}")
        )


def openai_result_emotion(sentence):
    messages = [
        {
            "role": "system",
            "content": "you are an assistant,"
            "give a human emotion response in one word only "
            "from encoding full daily task done by user and emotion should be understandable "
            "answer must not be in capital letters",
        }
    ]
    if sentence:
        messages.append(
            {"role": "user", "content": sentence},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        emotion_reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": emotion_reply})
        print(f"emotion from gpt - {emotion_reply}")
        return emotion_reply


@app.route("/logout", methods=["POST", "GET"])
def logout():
    try:
        session.pop("email", default=None)
        return render_template("login_page.html")
    except Exception as err:
        print(f"Caught an {err} in main file, logout function")
        return render_template(
            "index.html", status=html.unescape(f"you got error - {err}")
        )


if __name__ == "__main__":
    app.run(debug=False, port=2810)
