import pyautogui
import time
import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#mouseInfo = pyautogui.mouseInfo()

#simulate rank 1 click info, starting from the MEMBER RANK PAGE
#THIS IS JUST TO TEST IF IT WORKS, IT DOES 
'''
time.sleep(2)
pyautogui.click(753, 531, 1)
pyautogui.moveTo(604, 653, 1)
pyautogui.click()
pyautogui.moveTo(886, 849, 1)
pyautogui.click(interval=1)
pyautogui.screenshot("testkillstats.png")
pyautogui.mouseDown(1104, 827, button="left")
pyautogui.moveTo(1104, 444, 1)
pyautogui.mouseUp()
pyautogui.screenshot("testrssstats.png")
pyautogui.click(x=47, y=77, interval= 1, button="left")
pyautogui.click(x=47, y=77, interval= 1, button="left")
'''

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


'''
idRegion= 320, 450, 190, 50
cardRegion= 100, 275, 1690, 765
time.sleep(0.5)
click(750, 530) #Clicks player Icon
click(600, 650) #Clicks Info
#take_screenshot("playerCard.png", idRegion) #SS player Card
click(885, 850) #Clicks more Info
#take_screenshot("killStats.png", cardRegion) #SS kills
time.sleep(0.5)
click(47, 77) #Back arrow
click(47,77) #Back arrow
moveTo(750,530)
#tesseractRead() #Read from the 2 images
'''

'''
#Move to 2-4
click(750, 640) #2nd rank player
click(610, 750) #2nd rank info
click(885, 850) #2nd rank more info
click(47,77)
click(47,77)
moveTo(750,640)

click(750, 750) #3rd rank player
click(610, 420) #3rd rank info
'''

#Test Drag 5-8
drag(1215, 850, 1215, 410) #this works till the the account rank is higher than where it starts
    
    


# Need to figure out how to 1-4, scroll and repeat all the way till 200th member

#Once we reach 200th member, we can end if I use OCR to check if duplicate names appear