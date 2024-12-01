from difflib import SequenceMatcher

import cv2
import numpy as np
import pytesseract
import logging

from matplotlib import pyplot as plt

from config import tesseract_cmd, detailed_profile_screenshot_bound as ss_detail_bounds, player_screenshot_bound as ss_bounds
from objects import PlayersStats


logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

threshold = 0.8

def collectPlayerStats(detailedProfilePath, profileSummaryPath):
    name, currentPower, merits, victories, defeats, highestPower, kills, dead, healed = getPlayerDetails(detailedProfilePath)
    playerId = getPlayerSummary(profileSummaryPath)
    
    return PlayersStats(playerId, name, currentPower, merits, victories, defeats,  highestPower, kills, dead, healed)

#Most likely useless
def stringSimilarity(string1, string2):
    similarityRatio = SequenceMatcher(None, string1.lower(), string2.lower().ratio())
    
    return similarityRatio

#Grabs player data from more Info page
def getPlayerDetails(path):
    image = cv2.imread(path)
    
    name = readText(image, ss_detail_bounds["name"])
    currentPower = readNumber(image, ss_detail_bounds["current_power"])
    merits = readNumber(image, ss_detail_bounds["merits"])
    victories = readNumber(image, ss_detail_bounds["victories"])
    defeats = readNumber(image, ss_detail_bounds["defeats"])
    highestPower = readNumber(image, ss_detail_bounds["highest_power"])
    kills = readNumber(image, ss_detail_bounds["kills"])
    dead = readNumber(image, ss_detail_bounds["deads"])
    healed = readNumber(image, ss_detail_bounds["healed"])
    
    logging.info(f"Detail Name: {name}")
    logging.info(f"Current Power: {currentPower}")
    logging.info(f"Merits: {merits}")
    logging.info(f"Victories: {victories}")
    logging.info(f"Defeats: {defeats}")
    logging.info(f"highest Power: {highestPower}")
    logging.info(f"Kills: {kills}")
    logging.info(f"Dead: {dead}")
    logging.info(f"Healed: {healed}")
    
    return name, currentPower, merits, victories, defeats ,highestPower, kills, dead, healed

#Gets player Id from Info page
def getPlayerSummary(path):
    #read image
    image = cv2.imread(path)
    playerId = readGrayNumber(image, ss_bounds["playerId"])
    
    logging.error(f"Player Id: {playerId}")
    
    return playerId

#Reads numbers from config.py bounds
def readNumber(image, bounds):
    #crop the image based on bounding box coords
    croppedImage = image[bounds.y:bounds.y + bounds.height, bounds.x:bounds.x + bounds.width]
    
    #Grayscale image
    grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    
    #Apply adaptive thresholding to the grayscale image
    threshold_image = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    
    #Apply morphological transformations to enhance image
    kernel = np.ones((3,3), np.uint8)
    processedImage = cv2.morphologyEx(threshold_image, cv2.MORPH_CLOSE, kernel)
    
    #configure OCR
    customConfig = r'--oem 3 --psm 6 outputbase digits'
    
    #Perform OCR on processed image
    numbers = pytesseract.image_to_string(processedImage, config=customConfig)
    
    #Clean the OCR result to extract the number
    cleanedNumbers = ''.join(filter(lambda x: x.isdigit() or x == ',', numbers))

    #Formatting the number with commas
    try:
        extractedNumber = int(cleanedNumbers.replace(',', ''))
    except ValueError:
        extractedNumber = -1
        logging.error("OCR result doesn't contain valid number")
    
    return extractedNumber

#Read gray numbers from config.py bounds
def readGrayNumber(image, bounds):
    #Crop the image based on bounding box coords
    croppedImage = image[bounds.y:bounds.y + bounds.height, bounds.x:bounds.x + bounds.width]

    #Convert image to grayscale
    grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    
    #Apply Gaussian Filtering to reduce noise
    blurredImage = cv2.GaussianBlur(grayImage, (5, 5), 0)
    
    #Apply adaptive thresholding to blurred image
    threshold_image = cv2.adaptiveThreshold(blurredImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    #Configuring OCR
    customConfig = r'--oem 3 --psm 8 outputbase digits'
    
    #Perform OCR on threshold image
    numbers = pytesseract.image_to_string(threshold_image, config = customConfig)
    
    #Clean the OCR result to extract the number
    cleanedNumbers = ''.join(filter(lambda x: x.isdigit() or x == ',', numbers))
    
    return cleanedNumbers

#Read player with bounds from config.py
def readText(image, bounds):
    try:
        croppedImage = image[bounds.y:bounds.y + bounds.height, bounds.x:bounds.x + bounds.width]
        
        #Preprocess image
        grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        
        #Apply morphological operations to separate characters
        kernel = np.ones((2,2), np.uint8)
        dilatedImage = cv2.dilate(grayImage, kernel, iterations=1)
        erodedImage = cv2.erode(dilatedImage, kernel, iterations=1)
        
        customConfig = r'--oem 3 --psm 6 -l eng'
        text = pytesseract.image_to_string(erodedImage, config=customConfig)
        
        #Delete new line characters
        text = text.replace('\n', ' ')
        return text
    except Exception as e:
        logging.error(f"An error occurred during text extraction: {str(e)}")
        return ""