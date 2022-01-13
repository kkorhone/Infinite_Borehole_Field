import numpy as np
import os


def max_cap(label):
    toks = label.lower().split()
    caps = toks[0]
    for tok in toks[1:]:
        if tok in ["a", "an", "the", "of", "in", "on"]:
            caps += f" {tok}"
        else:
            caps += f" {tok.capitalize()}"
    return caps


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


def save_model(model, base_name="temp"):
    """Saves the specified model to disk prepending the specified base name and appending a running number."""
    for i in range(1000):
        file_name = f"{base_name.lower()}_{i:03d}.mph"
        if os.path.exists(file_name):
            print(f"File '{file_name}' already exists.")
        else:
            model.save(file_name)
            print(f"Saved model to file '{file_name}'.")
            return
    raise ValueError(f"Unable to save model using base name '{base_name.lower()}'.")
