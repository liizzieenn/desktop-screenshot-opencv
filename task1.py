import pyautogui
import cv2
import numpy as np

screenshot = pyautogui.screenshot()

screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
resized = cv2.resize(screenshot_cv, (800, 600))
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
cv2.imwrite("screenshot_gray.jpg", gray)

print("სქრინი წარმატებით შეინახა!")
