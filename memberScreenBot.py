import logging
import time
import os
import pyautogui
import pytesseract
import cv2
import numpy as np
import uuid
from PIL import Image
from mouse import drag, moveTo, moveClickTarget, click
from config import member_screen_coordinates

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#mouseInfo = pyautogui.mouseInfo()

def get_leader_screenshot(directory_path):
    new_path = os.path.join(directory_path, str(uuid.uuid4()))
    
    #open and close caching
    cell_position = member_screen_coordinates["leader_location"]
    click(cell_position)
    findImageClick("./rss/imfoButton.png")
    time.sleep(1)
    
    saveProfile(new_path)
    
    moveClickTarget(member_screen_coordinates["more_info_location"])
    time.sleep(1)
    moveClickTarget(member_screen_coordinates["back_button_location"])
    moveClickTarget(member_screen_coordinates["back_button_location"])

def findImageClick(reference_image_path, should_click=True, retry_count = 3, threshold = 0.8):
    for i in range(0, retry_count):
        #screenshot and save image
        bluestacks_screenshot = pyautogui.screenshot()
        bluestacks_screenshot.save('bluestacks_roi.png')
        
        #load up the screenshot
        screenshot = cv2.imread('bluestacks_roi.png')
        
        #load up reference image
        template = cv2.imread(reference_image_path)
        
        #perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
         # Check if a valid match is found based on the threshold
        if max_val >= threshold:
            # Get the coordinates of the top-left corner of the best match
            top_left = max_loc

            # Calculate the center of the reference image
            h, w = template.shape[:2]
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2

            # Simulate a click at the center of the reference image
            if should_click:
                pyautogui.click(center_x, center_y)
                time.sleep(.5)
            return True
        else:
            logging.info(
                f"No valid match found with confidence level below the threshold. Value: {max_val}, Threshold: {threshold}, Image:{reference_image_path},Count: {i}")
            time.sleep(.5)

    return False

def saveProfile(directory_path):
    try:
        os.makedirs(directory_path)
    finally:
        # Capture a screenshot of the BlueStacks screen within the ROI
        bluestacks_screenshot = pyautogui.screenshot()
        bluestacks_screenshot.save(os.path.join(directory_path, "profile_summary.png"))
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
