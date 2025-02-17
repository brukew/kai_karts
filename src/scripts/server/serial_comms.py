import serial
from logging import getLogger
from serial_read import read_packet
import globals

# TODO: multithreading for serial reader and proccessing (protect global variables)

SERIAL_PORT = "/dev/tty.usbmodem1401"
BAUD_RATE = 115200

logger = getLogger("SerialReader")

def init():
    try:
        globals.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logger.info(f"Opened serial port {SERIAL_PORT} at {BAUD_RATE} baud.")
        read_packet()
    except Exception as e:
        logger.error(f"Failed to open serial port {SERIAL_PORT}: {e}")
        return  # No point continuing if we can't open serial

if __name__ == "__main__":
    init()
