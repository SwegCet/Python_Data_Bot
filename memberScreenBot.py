import pyautogui
import time

mouseInfo = pyautogui.mouseInfo()

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
''' This is for rank 1
def click(x, y, duration=0.5, interval=0.1, button="left"):
    # Moves to a position and click
    pyautogui.moveTo(x,y, duration)
    pyautogui.click(interval=interval, button=button)
    
def drag(start_x, start_y, end_x, end_y, duration=1, button="left"):
    # Drags from one position to another holding left click
    pyautogui.mouseDown(start_x, start_y, button=button)
    pyautogui.moveTo(end_x, end_y, duration)
    pyautogui.mouseUp()
    
def take_screenshot(filename):
    # Takes a screenshot and saves it to the given filename
    pyautogui.screenshot(filename)
    

'''
# Need to figure out how to 1-4, scroll and repeat all the way till 200th member

#Once we reach 200th member, we can end if I use OCR to check if duplicate names appear