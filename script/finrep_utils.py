import datetime
from decimal import Decimal


def format_text(text):
    return text.replace('.', '').replace(',', '.')


def text_to_number(text):
    return Decimal(format_text(text))


def is_number(text):
    try:
        float(format_text(text))
        return True
    except ValueError:
        return False


def return_num_if_text_present(text):
    if is_number(text):
        number = text_to_number(text)
    else:
        number = None

    return number
