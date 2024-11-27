import pyautogui
import time
import os
import pytesseract
import cv2
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

mouseInfo = pyautogui.mouseInfo()

#SIMPLIFYING THE CODE W FUNCTIONS
def click(x, y, duration=1, interval=0.5, button="left"):
    # Moves to a position and click
    pyautogui.moveTo(x,y, duration)
    pyautogui.click(interval=interval, button=button)
    
def moveTo(x, y, duration=0.5):
    pyautogui.moveTo(x,y, duration) 
#This will move to the next rank (2-4)
def moveRelative(x, y, duration = 1):
#Move relative to the current position
    pyautogui.moveRel(x,y, duration)
    
# This scrolls up when we cleared ranks 1-4
def drag(start_x, start_y, end_x, end_y, duration=1, button="left"):
    time.sleep(0.5)
    # Drags from one position to another holding left click
    pyautogui.mouseDown(start_x, start_y, button=button)
    pyautogui.moveTo(end_x, end_y, duration)
    pyautogui.mouseDown(button="left")
    pyautogui.mouseUp()
    
def take_screenshot(filename, region=None):
    #Get current directory of script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    #define subfolder path
    subfolder = os.path.join(current_dir, "imgs")
    
    #sleep it for a second
    time.sleep(0.5)
    
    # Takes a screenshot and saves it to the given filename
    screenshot = pyautogui.screenshot(region=region)
    # Player Card Region (ONLY THE PLAYER ID): 320, 450, 190, 50
    #Player More info: 100, 275, 1690, 765
    
    #Save the screenshot in subfolder
    file_path = os.path.join(subfolder, filename)
    screenshot.save(file_path)

def tesseractRead():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subfolder = os.path.join(current_dir, "imgs")
    output_file = os.path.join(current_dir, "ocr_output.txt")
    
    #Open the output file in write mode
    with open(output_file, "w", encoding="utf-8") as f:
        for file_name in os.listdir(subfolder):
            if file_name.endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(subfolder, file_name)
                
                #Open image    
                img = Image.open(file_path)
                
                #perform OCR
                text = pytesseract.image_to_string(img)
                
                #Write output to the text file
                f.write(f"=== OCR Output for {file_name} ===\n")
                f.write(text + "\n\n")
                print(f"OCR processed for: {file_name}")


#simulate leader from the alliance members
'''
time.sleep(2)
click(830, 380)
click(770, 490)
take_screenshot("info.png")
click(880, 850)
take_screenshot("moreInfo.png")
click(40,80)
click(40,80)
'''

# Need to figure out how to 1-4, scroll and repeat all the way till 200th member

#Once we reach 200th member, we can end if I use OCR to check if duplicate names appear