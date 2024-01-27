"""
Module for control applications
"""

import time
import subprocess
import psutil
import pyautogui
import keyboard
import pytesseract
import pygetwindow as gw

class ProgramHandler:
    def __init__(self, app_path) -> None:
        self.app_path = app_path
        self.program = str(self.app_path).split('\\')[-1]
        self.opened = False

    def open_application(self):
        """
        Opens an application specified by the given path.

        Args:
            app_path (str): The path of the application.

        Returns:
            None
        """
        try:
            subprocess.Popen(self.app_path)
            # time.sleep(10)  # Wait seconds for the application to open
        except Exception as e:
            print(f"Error opening application: {e}")

    def close_application(self):
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == self.program:
                psutil.Process(process.info['pid']).terminate()
                self.opened = False
    
    def is_open_application(self):
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == self.program:
                self.opened = True
                return True
        return False

    def is_opened(self):
        return self.opened

    def maximize_window(self):
        """
        Maximizes the active window.

        Returns:
            None
        """
        try:
            pyautogui.hotkey("win", "up")
            time.sleep(2)
        except Exception as e:
            print(f"Error maximizing window: {e}")

    def click_coordinates(self, x, y, time_duration=0.5):
        """
        Moves the mouse to the specified coordinate and clicks.

        Args:
            x (int): The X coordinate.
            y (int): The Y coordinate.
            time_duration (float, optional): The duration of the mouse movement. Defaults to 0.5 seconds.

        Returns:
            None
        """
        try:
            if isinstance(x, int) and isinstance(y, int):
                pyautogui.moveTo(x, y, duration=time_duration)
                pyautogui.click()
            else:
                raise ValueError("Coordinates must be integers.")
        except Exception as e:
            print(f"Error clicking on coordinate: {e}")

    def double_click_coordinates(self, x, y, time_duration=0.5):
        """
        Moves the mouse to the specified coordinate and double-clicks.

        Args:
            x (int): The X coordinate.
            y (int): The Y coordinate.
            time_duration (float, optional): The duration of the mouse movement. Defaults to 0.5 seconds.

        Returns:
            None
        """
        try:
            if isinstance(x, int) and isinstance(y, int):
                pyautogui.moveTo(x, y, duration=time_duration)
                pyautogui.doubleClick()
            else:
                raise ValueError("Coordinates must be integers.")
        except Exception as e:
            print(f"Error double-clicking on coordinate: {e}")

    def write_text(self, text):
        """
        Writes text on the keyboard.

        Args:
            text (str): The text to write.

        Returns:
            None
        """
        try:
            pyautogui.write(text)
        except Exception as e:
            print(f"Error writing text: {e}")

    def press_key(self, key):
        """
        Presses a key on the keyboard.

        Args:
            key (str): The key to press.

        Returns:
            None
        """
        try:
            pyautogui.press(key)
        except Exception as e:
            print(f"Error pressing key: {e}")

    def press_keys(self, *keys):
        """
        Presses multiple keys on the keyboard at the same time.

        Args:
            keys (str): The keys to press.

        Returns:
            None
        """
        try:
            pyautogui.hotkey(*keys)
        except Exception as e:
            print(f"Error pressing keys: {e}")

    def freeze(self, seconds):
        """
        Freezes the program for the specified number of seconds.

        Args:
            seconds (int): The number of seconds to freeze.

        Returns:
            None
        """
        time.sleep(seconds)

    def mouse_position(self):
        """
        Gets the current position of the mouse.

        Returns:
            tuple: The current position of the mouse in format (x, y).
        """
        try:
            position = pyautogui.position()
            return position
        except Exception as e:
            print(f"Error getting mouse position: {e}")

    def mouse_position_on_key_press(self, key_to_monitor='space'):
        """
        Prints the mouse position each time a specific key is pressed.

        Args:
            key_to_monitor (str, optional): The key to monitor for key presses. Defaults to 'space'.
        """
        print(f"Press the '{key_to_monitor}' key to get mouse coordinates. Press 'esc' to stop monitoring.")
        counter = 1
        while True:
            # Check if the specified key is pressed
            if keyboard.is_pressed(key_to_monitor):
                x, y = self.mouse_position()
                print(f"{counter}. - {x}, {y}")
                counter += 1
                time.sleep(0.5)  # Prevents multiple prints if the key is held down

            # Check if the 'esc' key is pressed to stop the loop
            if keyboard.is_pressed('esc'):
                print("Monitoring stopped.")
                break

    def press_and_release_keys(self, keys):
        """
        Presses and releases the specified keys in order.

        Args:
            keys (list of str): The names of the keys.

        Returns:
            None
        """
        try:
            for key in keys:
                keyboard.press_and_release(key)
        except Exception as e:
            print(f"Error pressing and releasing keys: {e}")

    def press_key_kb(self, key):
        """
        Presses and holds the specified key.

        Args:
            key (str): The name of the key.

        Returns:
            None
        """
        try:
            keyboard.press(key)
        except Exception as e:
            print(f"Error pressing key: {e}")

    def release_key(self, key):
        """
        Releases the specified key.

        Args:
            key (str): The name of the key.

        Returns:
            None
        """
        try:
            keyboard.release(key)
        except Exception as e:
            print(f"Error releasing key: {e}")

    def key_name(self):
        """
        Identifies the name of the key being pressed.

        Returns:
            None
        """
        try:
            key = keyboard.read_key()
            print(f"You pressed: {key}")
        except Exception as e:
            print(f"Error identifying key: {e}")

    def get_screenshot(self, x, y, x_end, y_end):
        """
        Captures a screenshot within the specified region.

        Args:
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
            x_end (int): X-coordinate of the bottom-right corner.
            y_end (int): Y-coordinate of the bottom-right corner.

        Returns:
            PIL.Image.Image: The captured screenshot.
        """
        try:
            screenshot = pyautogui.screenshot(region=(x, y, x_end - x, y_end - y))
            return screenshot
        except Exception as e:
            print(f'Error with screenshot {e}')
            return f'Error: {e}'
        
    def perfom_ocr(self, image, language= 'eng'):
        """
        Performs Optical Character Recognition (OCR) on the given image.

        Args:
            image (PIL.Image.Image): The image to perform OCR on.
            language (str): The language code for OCR (default is 'eng').

        Returns:
            str: The extracted text from the image.
        """
        try:
            extracted_text = pytesseract.image_to_string(image, lang = language)
            return extracted_text
        except Exception as e:
            print(f'Error in OCR: {e}')
            return f'Error: {e}'
        
    def set_window(self, target_window_title, x, y):
        """
        Moves the specified window to the specified position.

        Args:
            target_window_title (str): The title of the window to be moved.
            x (int): The X-coordinate to move the window to.
            y (int): The Y-coordinate to move the window to.

        Returns:
            None
        """
        target_window = None
        window_list = gw.getAllTitles()
        for window_title in window_list:
            if target_window_title in window_title:
                target_window = gw.getWindowsWithTitle(window_title)[0]
                break
        if target_window:
            target_window.moveTo(x, y)
        else:
            print(f"Not found window with the title '{target_window_title}'")