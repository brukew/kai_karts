global ser
global kart_positions
global kart_data
global ITEM_INDEX
global ITEMS
global ITEM_TARGET
global END_INDEX
global seen_uids
global GAME_STATE_CHANGED

import threading
import random


SERIAL_PORT = "/dev/tty.usbmodem2101"
BAUD_RATE = 115200
ser = None

GAME_STATE_CHANGED = False

# Create a lock object.
global_lock = threading.Lock()

PACKET_LEN_BYTES = 24

# ordered list of kart positions
kart_positions = []

# State of karts {kart_id: {"index": track_index, "laps": int, "pos": (x, y)}}
kart_data = {}

ITEM_INDEX = {10, 25, 50}  # indices of item checkpoints
def points_within_circle(center, radius) -> set:
    """
    Returns a set of points (x,y) within a circle of given radius centered at center
    """
    points = set()
    center_x = center[0]
    center_y = center[1]
    for x in range(int(center_x - radius) - 1, int(center_x + radius) + 2):
        for y in range(int(center_y - radius) - 1, int(center_y + radius) + 2):
            if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                points.add((x, y))
    return points
multi_path_checkpoint = {"index": 50, "points": points_within_circle((30,40), 21)} # info about multi_path_checkpoint

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
    global kart_data, GAME_STATE_CHANGED
    with global_lock:
        print(f"Updating kart {kart_id} data: {new_data}")
        GAME_STATE_CHANGED = True
        kart_data[kart_id] = new_data

def update_kart_positions(new_positions):
    global kart_positions, GAME_STATE_CHANGED
    with global_lock:
        print(f"Updating kart positions - old: {kart_positions}, new: {new_positions}")
        GAME_STATE_CHANGED = True
        kart_positions = new_positions

def get_kart_data():
    with global_lock:
        return kart_data

def get_kart_positions():
    with global_lock:
        return kart_positions
    
def get_uid():
    return random.getrandbits(32)