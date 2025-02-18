import serial
from logging import getLogger
from .serial_read import read_packet
from . import globals
from concurrent.futures import ThreadPoolExecutor
from .test_input import input_init
import time

executor = ThreadPoolExecutor(max_workers=10)

logger = getLogger("SerialReader")

def init():
    try:
        globals.ser = serial.Serial(globals.SERIAL_PORT, globals.BAUD_RATE, timeout=1)
        print(f"Opened serial port {globals.SERIAL_PORT} at {globals.BAUD_RATE} baud.")
    except Exception as e:
        logger.error(f"Failed to open serial port {globals.SERIAL_PORT}: {e}")
        return  # No point continuing if we can't open serial
    print("Init input test.")
    input_init(executor)
    while True:
        # print("Reading packet.")
        packet = read_packet(executor)
        time.sleep(0.01)
        if packet is None:
            continue 