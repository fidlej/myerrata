
def valid_int(value):
    """Converts the value to an integer value or zero.
    """
    try:
        result = int(value)
    except ValueError:
        result = 0

    return result

