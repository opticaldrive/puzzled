import json
import string
# whats the uuid module there it is
import uuid

def create_whiteboard(name:str):
    whiteboard_id = str(uuid.uuid4())
    print(f"Creating whiteboard: ID={whiteboard_id}, Name={name}")
    with open(f"data/{whiteboard_id}.json", 'w') as whiteboard_file:
        json.dump({"name": name, "id": whiteboard_id, "contents": []}, whiteboard_file, indent=4)
    return whiteboard_id  # return the ID for later use
# create_whiteboard("test")


def is_safe_name(name):
    """
    silly checking just in case pf, idt it'll be that good
    """

    allowed_chars = set(
        string.ascii_letters + string.digits + "_" + "-" + " "
    )
    return all(char in allowed_chars for char in name)# fancy 1 liner stuff


def get_whiteboard(id:str):
    """
    Get the whiteboard - the ID is in the URL(handle by flask)
    """

    try:
        with open(f"data/{id}.json", 'r') as whiteboard_file:
            return json.load(whiteboard_file)
    except FileNotFoundError:
        return None  # no such file yay - just have flask return 404 if its none

def clear_whiteboard(id:str):
    """
    we clear the file's contents
    this is NOT deleting the file btw
    """
    try:
        with open(f"data/{id}.json", 'w') as whiteboard_file:
            data = get_whiteboard(id)
            data['contents'] = []  # clear the contents
            json.dump(data, whiteboard_file, indent=4)
            print(f"Whiteboard {id} cleared.")
            # this should be somewhat impossible to do via thewebsite but someone fooling around with requests maybe :Sob:
    except FileNotFoundError:
        print(f"Whiteboard {id} not found. Cannot clear contents.")




def add_drawing_to_whiteboard(id:str, drawing_data:dict):
    """
    Add a drawing to the whiteboard and save it to the JSON
    """

    try:
        # First, read the existing data
        with open(f"data/{id}.json", 'r') as whiteboard_file:
            data = json.load(whiteboard_file)
        
        # Then, append the new drawing
        data['contents'].append(drawing_data)
        
        # Write the updated data back to the file
        with open(f"data/{id}.json", 'w') as whiteboard_file:
            json.dump(data, whiteboard_file, indent=4)
        
        print(f"Drawing added to whiteboard {id}.")
    except FileNotFoundError:
        print(f"Whiteboard {id} not found. Cannot add drawing.")
