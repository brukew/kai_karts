import logging
import os

# Create logs directory if needed
os.makedirs("logs", exist_ok=True)

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,  # set minimum logging level
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/server.log"),
        logging.StreamHandler()  # also print to console
    ]
)

# Optionally create a dedicated logger for your serial code
logger = logging.getLogger("SerialReader")