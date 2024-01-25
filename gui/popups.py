"""
Display a pop up message windows for quick messages and questions.
"""

import logging
import time
import PySimpleGUI as sg

logger = logging.getLogger('popup_logger')

def ok(message, title="CCAR_EOL", text_color=None, background_color=None, font=("Arial", 18)):
    """
    Display a simple popup window with OK button. Window remains open until OK is selected.

    Blocking call.

    Args:
        message (str): The message window text.
        title (str, optional) - The message window header. Defaults to 'CCAR_EOL'
        text_color (str, optional): The color of the window text. Keep it simple. Defaults to None.
        background_color (str, optional): The color of the window background. Keep it simple. Defaults to None.

    Returns:
        str - The 'OK' text when clicked or "" if window is closed.
    """
    try:
        return sg.popup(
            message,
            title=title,
            text_color=text_color,
            background_color=background_color,
            font=font
        )
    except Exception:
        logger.exception("An Exception occurred when displaying Ok popup window.")
        return ""

def yes_no(message, title="CCAR_EOL", text_color=None, background_color=None, font=("Arial", 18)):
    """
    Display a message window with Yes and No button options.

    Blocking call.

    Args:
        message (str): The message window text.
        title (str, optional): The message window header. Defaults to "CCAR_EOL".
        text_color (str, optional): The color of the window text. Keep it simple. Defaults to None.
        background_color (str, optional): The color of the window background. Keep it simple. Defaults to None.

    Returns:
        str: The text of the button selected by user; 'Yes' or 'No'. "" if the window is closed.
    """
    try:
        rsp = sg.popup_yes_no(
            message,
            title=title,
            text_color=text_color,
            background_color=background_color,
            font=font
        )
        logger.debug(f"Popup '{message}': {rsp}")
        if not rsp:
            return ""
        return rsp
    except Exception:
        logger.exception("An Exception occurred when displaying Yes No popup window.")
        return ""

def ok_cancel(message, title="CCAR_EOL", text_color=None, background_color=None, font=("Arial", 18)):
    """
    Display a message window with Ok and Cancel button options.

    Blocking call.

    Args:
        message (str): The message window text.
        title (str, optional): The message window header. Defaults to "CCAR_EOL".
        text_color (str, optional): The color of the window text. Keep it simple. Defaults to None.
        background_color (str, optional): The color of the window background. Keep it simple. Defaults to None.

    Returns:
        str: The text of the button selected by user; 'Ok' or 'Cancel'. "" if the window is closed.
    """
    try:
        rsp = sg.popup_ok_cancel(
            message,
            title=title,
            text_color=text_color,
            background_color=background_color,
            font=font
        )
        logger.debug(f"Popup '{message}': {rsp}")
        if not rsp:
            return ""
        return rsp
    except Exception:
        logger.exception(
            "An Exception occurred when displaying ok cancel popup window."
        )
        return ""

def notify(message, title="Message", fade_ms=0, display_ms=10000):
    """
    Display an auto closing fade in window in the tray area of the screen for informational purposes.

    Blocking operation until auto closes.

    Args:
        message (str): The message window text.
        title (str, optional): The title for the popup window. Defaults to "Message".
        fade_ms (int, optional): The milliseconds to fade in and out the window. Defaults to 0.
        display_ms (int, optional): The milliseconds to display the window. Defaults to 10000.
    """
    try:
        sg.popup_notify(
            message,
            title=title,
            display_duration_in_ms=display_ms,
            fade_in_duration=fade_ms,
        )
    except Exception:
        logger.exception("An Exception occurred when displaying notify popup window.")

def quick_msg(message, display_sec=10, text_color="white", background_color="black", font=("Arial", 18)):
    """
    Briefly display an auto closing message box with no buttons or header. Displayed in middle of screen.

    Non-blocking. Sweet!

    Args:
        message (str): The message window text.
        display_sec (int, optional): The number of seconds to display the window before auto closing. Defaults to 10.
        text_color (str, optional): The color of the window text. Keep it simple. Defaults to None.
        background_color (str, optional): The color of the window background. Keep it simple. Defaults to None.
        font (tuple(str, int), optional): The font type and text size of the message.
    """
    try:
        sg.popup_quick_message(
            message,
            auto_close_duration=display_sec,
            text_color=text_color,
            background_color=background_color,
            font=font
        )
        time.sleep(display_sec)
    except Exception:
        logger.exception("An Exception occurred when displaying quick message popup window.")

def serial(title="CCAR_EOL", text_color=None, background_color=None, font=("Arial", 18)):
    """
    Display a window that prompts the user to enter a serial number 

    Args:
        title (str, optional): The message window header. Defaults to "CCAR_EOL".
        text_color (str, optional): The color of the window text. Keep it simple. Defaults to None.
        background_color (str, optional): The color of the window background. Keep it simple. Defaults to None.
        font (tuple(str, int), optional): The font type and text size of the message.

    Returns:
        str: The serial number entered by the user. "" if the window is closed.
    """
    try:
        layout = [
            [sg.Text(text='Serial:', text_color=text_color, font=font), sg.Input(key='SerialKey')]
        ]
        window = sg.Window(title, layout, background_color=background_color, finalize=True)
        window['SerialKey'].bind("<Return>", "_Enter")

        while True:
            event, values = window.read()
            logger.debug(f"Popup serial '{event}': N/A")
            if event == sg.WINDOW_CLOSED:
                return ""
            elif event == "SerialKey" + "_Enter":
                str_serial = values['SerialKey']
                logger.debug(f"Popup '{event}': {str_serial}")
                return str_serial
    except Exception:
        logger.exception("An Exception occurred when displaying quick message popup window.")
        return ""

def image_yes_no(
        message, image_path, title="CCAR_EOL", text_color=None, background_color=None, font=("Arial", 18)):
    """
    Display a imagen window with Yes and No button options.

    Blocking call.

    Args:
        message (str): The message window text.
        image_path (str): The path to the image file.
        title (str, optional): The message window header. Defaults to "CCAR_EOL".
        text_color (str, optional): The color of the window text. Keep it simple. Defaults to None.
        background_color (str, optional): The color of the window background. Keep it simple. Defaults to None.
        font (tuple(str, int), optional): The font type and text size of the message.

    Returns:
        str: The text of the button selected by user; 'Yes' or 'No'. "" if the window is closed.
    """
    try:
        layout = [
            [sg.Text(message, text_color=text_color, font= font)],
            [sg.Image(filename=image_path)],
            [sg.Yes(button_color='green'), sg.No(button_color='red')]
        ]
        window = sg.Window(title, layout, background_color=background_color, finalize=True)
        
        while True:
            event, _= window.read()
            logger.debug(f"Popup '{message}': {event}")
            if event == sg.WIN_CLOSED:
                return ""
            else:
                return event
    except Exception:
        logger.exception(
            "An Exception occurred when displaying quick message popup window."
        )
        return ""