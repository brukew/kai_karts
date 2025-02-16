import serial
import json
import logging
from logging import getLogger
import time
from .central_command import command_center

# TODO: multithreading for serial reader and proccessing (protect global variables)

SERIAL_PORT = "/dev/tty.usbmodem1401"
BAUD_RATE = 115200

logger = getLogger("SerialReader")

def init():
    try:
        global ser
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logger.info(f"Opened serial port {SERIAL_PORT} at {BAUD_RATE} baud.")
        read()
    except Exception as e:
        logger.error(f"Failed to open serial port {SERIAL_PORT}: {e}")
        return  # No point continuing if we can't open serial

def read():
    while True:
        try:            
            line = ser.readline().decode('utf-8', errors='replace').strip()
            
            if not line:
                logger.debug("Received empty line from serial.")
                continue
            
            data = json.loads(line)  # can raise json.JSONDecodeError
            logger.info(f"Received valid JSON from serial: {data}")
            
            command_center(data)            

        except json.JSONDecodeError as jde:
            logger.warning(f"JSON parse error for line: {line} | {jde}")
        except serial.SerialException as se:
            logger.error(f"Serial exception encountered: {se}")
            break
        except Exception as e:
            # Catch-all for any other unexpected errors
            logger.exception(f"Unexpected error reading from serial: {e}")
            # Decide whether to continue or break
            break

        time.sleep(0.01)  # small delay to prevent busy-wait

    ser.close()
    logger.info("SerialReader main loop exited, serial port closed.")

def write(data):
    json_data = json.dump(data)
    ser.write(json_data)

if __name__ == "__main__":
    init()
    read()
