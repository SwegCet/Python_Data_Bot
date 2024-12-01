import logging
import time
import os

import pyautogui
import cv2
import numpy as np
import uuid

from skimage.metrics import structural_similarity as ssim
from objects import Point
from mouse import drag, moveClickTarget
from config import member_screen_coordinates

#mouseInfo = pyautogui.mouseInfo()

def getLeaderScreenshot(directory_path):
    new_path = os.path.join(directory_path, str(uuid.uuid4()))
    
    #open and close caching
    cell_position = member_screen_coordinates["leader_location"]
    moveClickTarget(cell_position)
    findImageClick("./rss/infoButton.png")
    time.sleep(1)
    
    saveProfile(new_path)
    
    moveClickTarget(member_screen_coordinates["more_info_location"])
    time.sleep(1.5)
    saveDetailedProfile(new_path)
    moveClickTarget(member_screen_coordinates["back_button_location"])
    moveClickTarget(member_screen_coordinates["back_button_location"])

def processRanks(directory_path):
    #get the leader first
    getLeaderScreenshot(directory_path)
    
    while True:
        findDownArrowClick()
        circles = circlesInArea()
        
        if circles is not None:
            getMemberScreenshots(circles, directory_path)
            
            #take a screenshot before dragging
            ssBefore = pyautogui.screenshot()
            ssBefore.save('ssBefore.png')
            
            drag(
                Point(member_screen_coordinates["start_cell"].x, member_screen_coordinates["start_cell"].y), 
                Point(member_screen_coordinates["start_cell"].x, member_screen_coordinates["start_cell"].y) #add -400 here when done with testing
                )
            time.sleep(0.5)
            
            ssAfter = pyautogui.screenshot()
            ssAfter.save('ssAfter.png')
            
            isSame = areScreenshotsSame('ssBefore.png','ssAfter.png')
            if isSame: 
                break
            deleteSS('ssBefore.png')
            deleteSS('ssAfter.png')
            deleteSS('bluestack_roi.png')

def circlesInArea():
    roiWidth = member_screen_coordinates["circle_search_area"]["w"]
    roiHeight = member_screen_coordinates["circle_search_area"]["h"]
    
    #Defining the radius for circle detection
    min_Radius = member_screen_coordinates["circle_properties"]["min_radius"]
    max_Radius = member_screen_coordinates["circle_properties"]["max_radius"]
    roiX = member_screen_coordinates["circle_search_area"]["x"]
    roiY = member_screen_coordinates["circle_search_area"]["y"]
    
    #capture a screenshot of the bluestack screen within ROI
    bluestack_screenshot = pyautogui.screenshot(region=(roiX,roiY, roiWidth,roiHeight))
    bluestack_screenshot.save('bluestack_roi.png')
    
    #load bluestack image within ROI
    bluestack_image = cv2.imread('bluestack_roi.png', cv2.IMREAD_GRAYSCALE)
    bluestack_image = cv2.medianBlur(bluestack_image, 5) # Applying median blur for noise reduction
    
    #Perform Hough Circle Transform for circle detection within the ROI
    circles = cv2.HoughCircles(bluestack_image, cv2.HOUGH_GRADIENT, dp=1, minDist= 50, param1 = 50, param2 = 25, minRadius = min_Radius, maxRadius = max_Radius)
    
    return circles

def getMemberScreenshots(circles, directory_path):
    roiX = member_screen_coordinates["circle_search_area"]["x"]
    roiY = member_screen_coordinates["circle_search_area"]["y"]
    circles = np.uint16(np.around(circles))
    
    #move the mouse to the center of each detected circle in the ROI
    for circle in circles[0, :]:
        new_path = os.path.join(directory_path, str(uuid.uuid4()))
        
        center = (circle[0] + roiX, circle[1] + roiY) 
        moveClickTarget(Point(center[0], center[1]), .1)
        
        if not findImageClick("./rss/infoButton.png"):
            continue
        time.sleep(1)
        
        saveProfile(new_path)
        
        #click more info
        moveClickTarget(member_screen_coordinates["more_info_location"])
        time.sleep(1.5)
        saveDetailedProfile(new_path)
        moveClickTarget(member_screen_coordinates["back_button_location"])
        moveClickTarget(member_screen_coordinates["back_button_location"])

def findImageClick(reference_image_path, should_click=True, retry_count = 3, threshold = 0.8):
    for i in range(0, retry_count):
        #screenshot and save image
        bluestacks_screenshot = pyautogui.screenshot()
        bluestacks_screenshot.save('bluestack_roi.png')
        
        #load up the screenshot
        screenshot = cv2.imread('bluestack_roi.png')
        
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
        
def saveDetailedProfile(directory_path):
    #capture a screenshot of bluestacks screen within the ROI 
    bluestacks_screenshot = pyautogui.screenshot()
    bluestacks_screenshot.save(os.path.join(directory_path, "detailed_profile.png"))

def deleteSS(path): 
    if os.path.exists(path):
        os.remove(path)

def areScreenshotsSame(beforepath, afterpath):
    #load screenshots for comparison
    imageBefore = cv2.imread(beforepath)
    imageAfter = cv2.imread(afterpath)
    
    #convert image to grayscale for comparsion
    grayBefore = cv2.cvtColor(imageBefore, cv2.COLOR_BGR2GRAY)
    grayAfter = cv2.cvtColor(imageAfter, cv2.COLOR_BGR2GRAY)
    
    #Calculate SSI between the 2 images
    ssiScore, _ = ssim(grayBefore, grayAfter, full = True)
    
    #Compare SSI score to determine if images are same
    threshold = 0.95
    if ssiScore > threshold:
        return True
    else:
        return False
      
def findDownArrowClick():
    referenceImage = './rss/downArrowButton.png'
    threshold = 0.95
    
    #capture screenshot
    bluestackSS = pyautogui.screenshot()
    bluestackSS.save('bluestack_roi.png')
    
    #load screenshot
    screenshot = cv2.imread('bluestack_roi.png')
    
    #load reference image
    template = cv2.imread(referenceImage)

    #perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    #set threshold for the match value to filter out less accurate amtches
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        #get coordinates of top left corner of best match
        topLeft = pt
         # Calculate the center of the reference image
        h, w = template.shape[:2]
        center_x = topLeft[0] + w // 2
        center_y = topLeft[1] + h // 2

        # Simulate a click at the center of the reference image
        pyautogui.click(center_x, center_y)
        time.sleep(0.5)  # Wait for the click action to take effect
        break