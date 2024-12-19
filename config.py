from objects import Point, ImageBounds

# CHANGE ALL COORDINATES FITTING WITH YOUR COORDINATES ON SCREEN
# TO GET COORDINATES, USE pyautogui.mouseInfo() IN memberScreenBot.py and RUN IT in that file

#Set boundaries for player stats and name, Highlights the NUMBERS for stats and NAME for player ONLY
#Format for coordiante is: ImageBounds(Point(X,Y), Xoffset, Yoffset) <- THIS CREATES A RECTANGLE "BOX" 
#Higher values of X offset = move right
#Higher values of Y offset = move down

detailed_profile_screenshot_bound = {
    "name": ImageBounds(Point(190, 690), 280, 50),
    "current_power": ImageBounds(Point(210, 805),250, 50),
    "merits": ImageBounds(Point(190, 935), 280, 60),
    "highest_power": ImageBounds(Point(1480, 390),210, 35),
    "victories": ImageBounds(Point(1560, 490), 130, 50),
    "defeats": ImageBounds(Point(1560, 550), 130, 50),
    "kills": ImageBounds(Point(1470, 710), 220, 35),
    "deads": ImageBounds(Point(1520, 760), 170, 35),
    "healed": ImageBounds(Point(1470, 810), 220, 35)
}

#Set boundaries for the player Id numbers
player_screenshot_bound = {
    "playerId": ImageBounds(Point(340,470), 130, 30)
}

#For Image Recognition
tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

member_screen_coordinates = {
    "leader_location": Point(830, 385), # Where the leader is
    "circle_search_area": { # Rectangular Area starting from top left of R4 tab rectangle to bottom Right of Members
        "x":730,
        "y":550,
        "w":1100, #730 + 1100
        "h": 410, #290 + 670
    },
    "start_cell": Point(1275, 785), # Starts at the gap between members (empty space)
    "circle_properties": {
        "min_radius": 35,
        "max_radius": 55,
    },
    #These two are always in the same spot
    "back_button_location":Point(40,80), # Back Button Location
    "more_info_location": Point(880, 850) # More Info Button Location
}