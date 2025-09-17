import json
import os

# Define the name of the file where data will be stored
DATA_FILE = "tracked_series.json"

def load_data():
    """
    Loads tracked series data from the local JSON file.

    Returns:
        dict: A dictionary containing the user's tracked series.
              Returns an empty dictionary if the file doesn't exist.
    """
    # Check if the data file exists
    if os.path.exists(DATA_FILE):
        # If it exists, open the file and load the JSON content
        with open(DATA_FILE, "r") as f:
            try:
                # Attempt to load the JSON data
                return json.load(f)
            except json.JSONDecodeError:
                # Handle the case where the file is empty or corrupted
                print(f"Warning: {DATA_FILE} is empty or corrupted. Creating a new file.")
                return {}
    else:
        # If the file doesn't exist, return an empty dictionary to start fresh
        return {}

def save_data(data):
    """
    Saves the provided data to the local JSON file.

    Args:
        data (dict): The dictionary containing the series to be saved.
    """
    # Open the file in write mode and dump the JSON data with formatting
    with open(DATA_FILE, "w") as f:
        # `indent=4` makes the JSON file nicely formatted and easy to read
        json.dump(data, f, indent=4)
    print("Data saved successfully.")

# --- Example of a typical data structure saved in the JSON file ---
# {
#     "asura": {
#         "series_title_1": {
#             "url": "https://asurascans.com/series/title-1",
#             "last_chapter": 15
#         },
#         "series_title_2": {
#             "url": "https://asurascans.com/series/title-2",
#             "last_chapter": 24
#         }
#     },
#     "flame": {
#         "series_title_3": {
#             "url": "https://flamescans.org/series/title-3",
#             "last_chapter": 56
#         }
#     }
# }