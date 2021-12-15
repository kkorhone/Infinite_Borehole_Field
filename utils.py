import numpy as np
import os


def num_to_str(num, decimals=3):
    """Makes a nice string out of the specified number."""
    if num == int(num):
        return str(int(num))
    else:
        return str(round(num, decimals))

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
