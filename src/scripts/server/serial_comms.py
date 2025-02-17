import serial
from logging import getLogger
from serial_read import read_packet, start_read
import globals
from concurrent.futures import ThreadPoolExecutor


# Create a pool with a fixed number of worker threads.
executor = ThreadPoolExecutor(max_workers=10)

SERIAL_PORT = "/dev/tty.usbmodem1401"
BAUD_RATE = 115200

logger = getLogger("SerialReader")

def init():
    try:
        globals.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logger.info(f"Opened serial port {SERIAL_PORT} at {BAUD_RATE} baud.")
        while True:
            packet = read_packet(executor)
            if packet is None:
                continue 
        # start_read()
        # thread = threading.Thread(target=read_packet)
        # thread.start()
    except Exception as e:
        logger.error(f"Failed to open serial port {SERIAL_PORT}: {e}")
        return  # No point continuing if we can't open serial
