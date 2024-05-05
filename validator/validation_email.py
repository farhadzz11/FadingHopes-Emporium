from re import compile


def is_valid_email(email: str) -> dict:
    email_pattern = compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@(gmail.com|yahoo.com)$")

    if not email_pattern.match(email):
        return {"valid": False, "message": "The email address you entered is invalid. Please check the format of your "
                                           "email address and try again\nOnly email addresses with the domains "
                                           "gmail.com or yahoo.com are allowed"}

    if not (5 < len(email.split('@')[0]) < 33):
        return {"valid": False, "message": "The username of email you entered is too long or too short. The maximum "
                                           "length is 32 characters.\nThe minimum length is 6 characters."}

    return {"valid": True, "message": "The email is valid"}
