import pyautogui
import time


def moveTo(location, duration=0.1):
    pyautogui.moveTo(location.x, location.y, duration)
    time.sleep(.1)


def click():
    pyautogui.click()


def moveClickTarget(location, duration=0.1):
    moveTo(location, duration)
    click()
    time.sleep(.3)


def drag(source_location, target_location, drag_duration=1):
    moveTo(source_location)
    pyautogui.mouseDown()
    moveTo(target_location, drag_duration)
    pyautogui.mouseUp()