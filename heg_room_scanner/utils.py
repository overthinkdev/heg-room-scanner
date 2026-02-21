def format_room_display(room):
    return room[0].upper() + "." + room[1:]

def display_to_query(room_display):
    return room_display.replace(".", "").lower()
