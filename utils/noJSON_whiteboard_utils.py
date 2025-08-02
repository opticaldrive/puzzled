import string
import uuid

# In-memory storage for whiteboards
whiteboards = {}

def create_whiteboard(name: str):
    whiteboard_id = str(uuid.uuid4())
    print(f"Creating whiteboard: ID={whiteboard_id}, Name={name}")
    whiteboards[whiteboard_id] = {"name": name, "id": whiteboard_id, "contents": []}
    return whiteboard_id  # return the ID for later use

def is_safe_name(name):
    """
    Check if the name contains only allowed characters.
    """
    allowed_chars = set(string.ascii_letters + string.digits + "_" + "-" + " ")
    return all(char in allowed_chars for char in name)

def get_whiteboard(id: str):
    """
    Get the whiteboard by ID.
    """
    return whiteboards.get(id)  # returns None if the ID does not exist

def clear_whiteboard(id: str):
    """
    Clear the contents of the whiteboard.
    """
    if id in whiteboards:
        whiteboards[id]['contents'] = []  # clear the contents
        print(f"Whiteboard {id} cleared.")
    else:
        print(f"Whiteboard {id} not found. Cannot clear contents.")

def add_drawing_to_whiteboard(id: str, drawing_data: dict):
    """
    Add a drawing to the whiteboard.
    """
    if id in whiteboards:
        whiteboards[id]['contents'].append(drawing_data)
        print(f"Drawing added to whiteboard {id}.")
    else:
        print(f"Whiteboard {id} not found. Cannot add drawing.")

# Example usage
# whiteboard_id = create_whiteboard("test")
# add_drawing_to_whiteboard(whiteboard_id, {"type": "circle", "color": "red"})
# print(get_whiteboard(whiteboard_id))
# clear_whiteboard(whiteboard_id)
