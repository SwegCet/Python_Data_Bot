from objects import Point, ImageBounds

#Set boundaries for player stats and name, Highlights the NUMBERS for stats and NAME for player ONLY
detailed_profile_screenshot_bound = {
    "name": ImageBounds(Point(210, 690), 280, 50),
    "current_power": ImageBounds(Point(210, 805),250, 40),
    "merits": ImageBounds(Point(210, 935), 250, 40),
    "highest_power": ImageBounds(Point(1480, 390),210, 30),
    "victories": ImageBounds(Point(1560, 490), 130, 40),
    "defeats": ImageBounds(Point(1560, 550), 130, 40),
    "kills": ImageBounds(Point(1470, 710), 220, 30),
    "deads": ImageBounds(Point(1520, 760), 170, 30),
    "healed": ImageBounds(Point(1470, 810), 220, 30)
}

#Set boundaries for the player Id numbers
player_screenshot_bound = {
    "player_id": ImageBounds(Point(360,470), 150, 30)
}

#For Image Recognition
tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

member_screen_coordinates = {
    "leader_location": Point(830, 385), # Where the leader is
    "circle_search_area": { # Rectangular Area starting from top left of leader row to bottom right most corner of member row
        "x":730,
        "y":290,
        "w":1100, #730 + 1100
        "h": 670, #290 + 670
    },
    "start_cell": Point(960, 540), # Starts at middle of screen (Change if resolution is not 1920x1080)
    "circle_properties": {
        "min_radius": 35,
        "max_radius": 55,
    },
    #These two are always in the same spot
    "back_button_location":Point(40,80), # Back Button Location
    "more_info_location": Point(880, 850) # More Info Button Location
}