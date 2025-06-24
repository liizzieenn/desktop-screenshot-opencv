import cv2
import numpy as np
import pyautogui
import time
import mss
from PIL import Image

CURSOR_PATH = "cursor.png"
cursor_img = cv2.imread(CURSOR_PATH, cv2.IMREAD_UNCHANGED)

def overlay_cursor(background, cursor, x, y):
    """ამატებს კურსორის PNGს სქრინზე შესაბამის პოზიციაზე (სკეილინგით)"""
    ch, cw = cursor.shape[:2]
    for c in range(0, 3):  # RGB არხებზე
        background[y:y+ch, x:x+cw, c] = (
            cursor[:, :, c] * (cursor[:, :, 3] / 255.0) +
            background[y:y+ch, x:x+cw, c] * (1.0 - cursor[:, :, 3] / 255.0)
        )
    return background

while True:
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_np = np.array(img)
        original_h, original_w = img_np.shape[:2]
        resized = cv2.resize(img_np, (800, 600))

        mouse_x, mouse_y = pyautogui.position()

        scale_x = 800 / original_w
        scale_y = 600 / original_h
        cursor_x = int(mouse_x * scale_x)
        cursor_y = int(mouse_y * scale_y)

        resized_bgra = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)

        if cursor_img is not None:
            ch, cw = cursor_img.shape[:2]
            if 0 <= cursor_x <= (800 - cw) and 0 <= cursor_y <= (600 - ch):
                resized_bgra = overlay_cursor(resized_bgra, cursor_img, cursor_x, cursor_y)

        gray = cv2.cvtColor(resized_bgra, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("screenshot_gray.jpg", gray)
        print("ახალი სქრინი შეინახა!")

    time.sleep(30)
