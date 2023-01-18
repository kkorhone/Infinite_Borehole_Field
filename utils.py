import numpy as np


def num_to_str(num):
    """Makes a nice string out of the specified number."""
    if num == 0:
        return "0"
    else:
        dec = 6 - int(np.ceil(np.log10(abs(num))))
        if dec > 0:
            return str(round(num, dec))
        else:
            return str(int(num))


def time_elapsed(seconds):
    """Formats seconds as XmYs."""
    seconds = int(np.floor(seconds))
    minutes = seconds // 60
    seconds %= 60
    if minutes == 0:
        return f"{seconds}s"
    elif seconds == 0:
        return f"{minutes}m"
    return f"{minutes}m{seconds}s"
