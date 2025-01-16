import json
import logging
import os
import threading
from pathlib import Path
from typing import Optional, TypedDict

# import pystray
from bottle import Bottle, get, post, request, route, run
from infi.systray import SysTrayIcon

# from PIL import Image
from win11toast import notify


class Config(TypedDict):
    host: str
    port: int


DEBUG = False
BASE_PATH = Path(__file__).parent
ICON_PATH_PNG = BASE_PATH / "appicon.png"
ICON_PATH_ICO = BASE_PATH / "appicon.ico"
CONFIG_PATH = BASE_PATH / "config.json"
DEFAULT_CONFIG: Config = {"host": "0.0.0.0", "port": 8081}


# Set up logging
logging_level = (
    logging.DEBUG if DEBUG else logging.CRITICAL
)  # Conditionally set logging level
logging.basicConfig(
    level=logging_level,  # Set logging level based on DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
    ],
)
logger = logging.getLogger()


def validate_config(config: dict) -> Config:
    """
    Validate the loaded configuration against the expected types.
    If the validation fails, return default values.
    """
    if not isinstance(config.get("host"), str):
        logger.error(
            f"Invalid type for 'host': expected str, got {type(config.get('host'))}"
        )
        host = DEFAULT_CONFIG["host"]
    if not isinstance(config.get("port"), int):
        logger.error(
            f"Invalid type for 'port': expected int, got {type(config.get('port'))}"
        )
        port = DEFAULT_CONFIG["port"]
    return {"host": host, "port": port}


def load_config() -> Config:
    """
    Load configuration from the 'config.json' file. If the file is missing or
    malformed, return default values for host and port.

    Returns:
        dict: A dictionary containing configuration settings with keys "host", "port".
    """
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

        validated_config = validate_config(config)
        logger.debug("Config loaded and validated successfully.")
        return validated_config

    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return DEFAULT_CONFIG  # Return default values on error


def show_notification(
    title: str = "Hello", body_message: str = "Hello from Python"
) -> None:
    """
    Show a Windows 11-style notification using the 'win11toast' library.
    This function will trigger a notification with a message and an icon.

    If any error occurs during notification creation, it will be caught and ignored.
    """
    try:
        icon = {"src": f"file://{ICON_PATH_PNG}", "placement": "appLogoOverride"}
        notify(title, body_message, icon=icon)
        logger.debug(f"Notification triggered: {title} - {body_message}")
    except Exception as e:
        logger.error(f"Error showing notification: {e}")
        pass


# Read configuration from config.json
config = load_config()

app = Bottle()


@route("/")
def home() -> str:
    return "notification server is online"


# Bottle route that triggers a notification
@get("/notification")
def get_notification() -> str:
    return "wrong method"


@post("/notification")
def post_notification() -> str | tuple[str, Optional[int]]:
    """
    Bottle route that triggers a notification. This function starts a new
    thread to call the show_notification() function without blocking the main server thread.

    Returns:
        str: A simple response message indicating the notification was triggered.
    """
    logger.debug("Received POST request to trigger notification.")

    # Parse JSON data from the request body
    try:
        data = request.json  # This will parse the incoming JSON data
        if isinstance(data, dict):
            logger.info(f"data - {data}")
            title = data.get("title", "Notification request received")
            body = data.get("body_message", "Check calendar for more information")
            logger.info(f"Notification details: Title - {title}, Body - {body}")
        else:
            raise ValueError("No JSON data provided")
    except Exception as e:
        logger.error(f"Error parsing JSON data: {e}")
        return (
            "Invalid JSON data",
            400,
        )  # Return a 400 Bad Request if JSON parsing fails

    # Trigger notification in a separate thread
    threading.Thread(target=show_notification, args=(title, body)).start()

    return "Notification triggered"


def run_bottle_app() -> None:
    """
    Function to run the Bottle web application. It listens for HTTP requests
    on the host and port specified in the configuration.

    The application runs in a separate thread, and the Bottle server runs indefinitely
    until the application is terminated.
    """
    logger.info(
        f"Starting Bottle app on {config['host']}:{config['port']}. Debug mode: {DEBUG}"
    )
    run(host=config["host"], port=config["port"], debug=DEBUG)


def on_quit(tryicon) -> None:
    """
    Handler function for quitting the system tray application. This function stops
    the tray icon and forcefully exits the program.

    Args:
        tryicon (pystray.Icon): The system tray icon.
        item (pystray.MenuItem): The selected menu item (in this case, "Quit").
    """
    logger.info("Exiting application...")
    # Force exit the application, which will terminate the Bottle server and main thread
    os._exit(0)


if __name__ == "__main__":
    """
    Main entry point for the application. This starts the Bottle app in a separate thread
    and the system tray application. The program will keep running until the user quits
    the tray application.
    """
    # Start Bottle app in a separate thread
    bottle_thread = threading.Thread(target=run_bottle_app, daemon=True)
    bottle_thread.start()

    # Start the tray application
    logger.info("Starting system tray application.")
    menu_options = ()
    systray = SysTrayIcon(str(ICON_PATH_ICO), "Quit", menu_options, on_quit=on_quit)
    systray.start()
