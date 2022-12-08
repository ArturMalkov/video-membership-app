from email_validator import EmailNotValidError, validate_email


def _validate_email(email):
    message = ""
    valid = False
    try:
        valid = validate_email(email)
        # update the email variable with a normalized value
        email = valid.email
        valid = True
    except EmailNotValidError as err:
        message = str(err)

    return valid, message, email
