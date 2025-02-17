global ser
global kart_positions
global kart_data
global ITEM_INDEX
global ITEMS
global ITEM_TARGET
global END_INDEX
global seen_uids

import threading

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
    "banana": {"target":[-1]}, # 0% chance for last
    "bob-omb": {"target":[1, 2, 3]}, # 0% chance for first
    "red_shroom": {"target":[0]},
    "lightning": {"target":"all"},
    "bullet_bill": {"target":[0]},
    "gold_shroom": {"target":[0]}, 
    "red_shell": {"target":[1]}, # 0% chance for first
    "blue_shell": {"target":"first"}
}

# TODO: Finish Line Index
END_INDEX = 2000  # track position that indicates a lap crossing

seen_uids = set()

def update_kart_data(kart_id, new_data):
    global kart_data
    with global_lock:
        kart_data[kart_id] = new_data

def update_kart_positions(new_positions):
    global kart_positions
    with global_lock:
        kart_positions = new_positions

def get_kart_data():
    with global_lock:
        return kart_data

def get_kart_positions():
    with global_lock:
        return kart_positions