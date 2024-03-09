from email_validator import validate_email, EmailNotValidError
from validate_email import validate_email
import re


def validating_email(enter_email):
    try:
        is_valid = validate_email(enter_email)
        if is_valid:
            return {'True': enter_email}
        else:
            return {'False': enter_email}
    except EmailNotValidError as email_err:
        print(f"Caught an error in email verification - {email_err}")


def validating_password(input_pass):
    try:
        if not re.search('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,10}$', input_pass):
            return False
        return True
    except Exception as err:
        print(str(err))

    return input_pass
