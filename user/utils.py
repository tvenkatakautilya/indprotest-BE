import re


def is_valid_user_name(username):
    # Check if the username is valid (e.g., meets certain criteria)
    # For example, check if it contains only alphanumeric characters
    return re.match(r"^[a-zA-Z0-9_]{3,}$", username) is not None


def is_valid_email_id(email):
    # Check if the email is valid (e.g., meets certain criteria)
    # For example, check if it has a valid format
    return (
        re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None
    )


def is_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$"
    if re.match(pattern, password):
        return True
    return False
