'''Ignore user Invalid ENTRy'''

import requests


class MinMaxRange(Exception):
    """Custom Error"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def read_text(prompt):
    '''Display a prompt reads string in text
    Keyboard Interrupts (Ctrl + C) are ignored
    returns a string containing string entered by user '''
    while True:
        try:
            result = input(prompt)
            # if we get here no exception has raised
            if result == '':
                print('Please do not leave empty')
            else:  # break out of loop
                return result
        except KeyboardInterrupt:  # if we get here user entered Ctrl + C
            print('Do interrupt the process')


def read_number(prompt, function):
    '''Display a prompt and read int or floating point number
    Keyboard Interrupts are ignored
    Invalid numbers are rejected and only returns a number containing the value input by user'''
    message = ["Please enter a integer number", "Please enter a float number"]
    if isinstance(function, int):
        warning = message[0]
    if isinstance(function, float):
        warning = message[1]
    else:
        warning = "!!!!INVALID ENTRY!!!!"
    while True:
        try:
            number_text = read_text(prompt)
            # this the where it is confirmed or raises exception
            result = function(number_text)
            return result
        except ValueError:
            print(warning)


def read_number_ranged(prompt, function, min_value, max_value):
    '''
    Displays a prompt and reads in a number.
    min_value gives the inclusive minimum value
    max_value gives the inclusive maximum value
    Raises an exception if max and min are the wrong way round
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a number containing the value input by the user
    '''
    if min_value > max_value:  # checking min and max value range
        raise MinMaxRange('Min value is greater than Max value')
    while True:
        result = read_number(prompt, function)
        if result < min_value:  # if entry is smaller than minimum value range
            print(
                f'Number you have entered lower than minimum value\nMin value is {min_value}')
            continue
        elif result > max_value:  # if entry is greater than maximum value range
            print(
                f'Number you have entered greater than maximum value\nMax value is {max_value}')
            continue
        return result


def read_float(prompt):
    '''
    Displays a prompt and reads in a floating point number.
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a float containing the value input by the user
    '''
    return read_number(prompt, float)


def read_int(prompt):
    '''
    Displays a prompt and reads in an integer number.
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns an int containing the value input by the user
    '''
    return read_number(prompt, int)


def read_float_ranged(prompt, min_value, max_value):
    '''
    Displays a prompt and reads in a floating point number.
    min_value gives the inclusive minimum value
    max_value gives the inclusive maximum value
    Raises an exception if max and min are the wrong way round
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a number containing the value input by the user
    '''
    return read_number_ranged(prompt, float, min_value, max_value)


def read_int_ranged(prompt, min_value, max_value):
    '''
    Displays a prompt and reads in an integer point number.
    min_value gives the inclusive minimum value
    max_value gives the inclusive maximum value
    Raises an exception if max and min are the wrong way round
    Keyboard interrupts (CTRL+C) are ignored
    Invalid numbers are rejected
    returns a number containing the value input by the user
    '''
    return read_number_ranged(prompt, int, min_value, max_value)


def ask_to_continue(prompt):
    '''Save time every time ask a continue'''
    ask = input(prompt)
    return 'y' in ask.lower()


def page_request(url):
    """Error Handled Requests"""
    try:
        result = requests.get(url, timeout=10)
        result.raise_for_status()
        return result
    except requests.exceptions.RequestException as exc:
        print(f"Error requesting page {url}: {exc}")
        return None


def convert_to_string(data):
    """Converts data to string"""
    if isinstance(data, str):
        return data
    if callable(data):
        return data.__name__
    if isinstance(data, (int, float)):
        return str(data)
    return None
