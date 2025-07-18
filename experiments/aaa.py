from utils.whiteboard_utils import create_whiteboard, get_whiteboard, clear_whiteboard, add_drawing_to_whiteboard

id = create_whiteboard("kaboom")  # Example usage, can be removed later
print(get_whiteboard(id))
add_drawing_to_whiteboard(id, {"type": "line", "data": {"x1": 0, "y1": 0, "x2": 100, "y2": 100}})