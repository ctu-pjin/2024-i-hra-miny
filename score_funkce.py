import json
from random import choice
import math


"""Score system functions"""
# Generate a unique ID
def create_id(id_range):
    id = ""
    values = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
    for _ in range(id_range):
        id += chr(choice(values))
    return id


# Save data to JSON file
def save_data(data):
    try:
        with open("scores.json", 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")


# Load data from JSON file
def get_data():
    try:
        with open("scores.json", 'r') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, ValueError, FileNotFoundError):
        return {}


def update_or_add_game_data(width, height, num_mines):
    key = str((width, height, num_mines)) 
    data = get_data() 

    # Creates basic times if the field of the definied parameters does not exist
    if key not in data:
        medal_times = {
        "gold": {"username": "gold", "time": str(int(math.sqrt(width * height) * num_mines /2))},
            "silver": {"username": "silver", "time": str(int(math.sqrt(width * height) * num_mines))},
            "bronze": {"username": "bronze", "time": str(int(math.sqrt(width * height) * num_mines * 2))}
        }
        data[key] = medal_times 
        
        save_data(data) 

    return data


def add_user_score(width, height, num_mines, username, time):
    key = str((width, height, num_mines))  
    data = get_data()  

    if key not in data:
        print("Game parameters not found. Initializing new game data.")
        data = update_or_add_game_data(width, height, num_mines)

    user_id = create_id(20)  # Generate a unique ID for the user

    data[key][user_id] = {
        "username": username,
        "time": str(round(time, 1))
    }

    save_data(data)  
    return data[key]  


def show_data(data_dict):
    # Shows the game leaderboard
    print("\n------LEADERBOARD------")
    try:
        # Sort the participants by their 'time' field
        sorted_scores = sorted(data_dict.values(), key=lambda x: float(x["time"]))
    except (TypeError, KeyError) as e:
        print("Error: Invalid data structure or missing keys. Please check the input data.")
        print(f"Details: {e}")
    print()
    return sorted_scores


def create_str_key(list_of_int):
    str_key = "(" + str(list_of_int[0]) + ", " + str(list_of_int[1]) + ", " + str(list_of_int[2]) + ")"
    return str_key


def check_for_difficulty(str_input):
    diffs = ["easy", "medium", "hard"]
    if str_input.lower() in diffs:
        return True
    else:
        return False 