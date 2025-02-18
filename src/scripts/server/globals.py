global ser
global kart_positions
global kart_data
global ITEM_INDEX
global ITEMS
global ITEM_TARGET
global END_INDEX
global seen_uids

import threading
import random


SERIAL_PORT = "/dev/tty.usbmodem1301"
BAUD_RATE = 115200
ser = None

# Create a lock object.
global_lock = threading.Lock()

PACKET_LEN_BYTES = 24

# ordered list of kart positions
kart_positions = []

# State of karts {kart_id: {"index": track_index, "laps": int}}
kart_data = {}

ITEM_INDEX = {10, 25, 50}  # example track positions

# Items
ITEMS = ["banana", "bob-omb", "red_shroom", "lightning", "bullet_bill", "gold_shroom", "red_shell", "blue_shell"]

# ['Banana', 'Bomb', 'redShroom', 'goldShroom', 'redShell', 'blueShell', 'lightning', 'bulletBill']

#   A dict that maps item names to their targets relative to the player that used it
ITEM_TARGET = {
    "banana": [-1], # 0% chance for last
    "bob-omb": [1, 2, 3], # 0% chance for first
    "red_shroom": [0],
    "lightning": "all",
    "bullet_bill": [0],
    "gold_shroom": [0], 
    "red_shell": [1], # 0% chance for first
    "blue_shell": "first"
}

# TODO: Finish Line Index
END_INDEX = 2000  # track position that indicates a lap crossing

seen_uids = set()

def update_kart_data(kart_id, new_data):
    global kart_data
    with global_lock:
        print(f"Updating kart {kart_id} data: {new_data}")
        kart_data[kart_id] = new_data

def update_kart_positions(new_positions):
    global kart_positions
    with global_lock:
        print(f"Updating kart positions - old: {kart_positions}, new: {new_positions}")
        kart_positions = new_positions

def get_kart_data():
    with global_lock:
        return kart_data

def get_kart_positions():
    with global_lock:
        return kart_positions
    
def get_uid():
    return random.getrandbits(32)