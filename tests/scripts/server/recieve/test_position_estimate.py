#!/usr/bin/env python3
import os
import uuid
import logging
from collections import defaultdict

# --- Setup Logging ---
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger()

# --- Global State (simulate server/utils.py) ---
# For simplicity, assume track indices range from 0 to END_INDEX.
END_INDEX = 500
# Example: Checkpoints are at indices 10, 25, and 50.
ITEM_INDEX = {150, 300, 450}

# We'll use a dict for kart_data. Each entry: {kart_id: {"index": int, "laps": int, "position": (x, y)}}
kart_data = {}

# We'll use a list for ranking; leader is at index 0.
kart_positions = []

def select_item_for_kart(kart_id):
    """
    For testing, simply return a fixed item.
    In a real scenario, you'd choose an item based on rank and weighting.
    """
    return "banana"

def update_rankings():
    """
    For testing, recalculate kart_positions based on 'laps' and 'index'.
    Leader: higher lap count, then higher index.
    """
    global kart_positions
    # Sort kart_data keys (kart_ids) descending by (laps, index)
    kart_positions = sorted(kart_data.keys(), key=lambda k: (kart_data[k]["laps"], kart_data[k]["index"]), reverse=True)
    logger.info(f"Updated rankings: {kart_positions}")

# --- Dummy send_item (simulate server/send/send_item.py) ---
def send_item(kart_id, item, event_uid):
    logger.info(f"send_item called: Kart {kart_id} receives '{item}' (event_uid: {event_uid})")

# --- Your Functions Under Test ---
FINISH_LINE_ERROR = 0.8

def check_cross_finish(old_ix, new_ix) -> bool:
    '''Return True if the difference between old_ix and new_ix indicates a finish-line crossing.
       Assume indices wrap around at END_INDEX.
    '''
    diff = (old_ix - new_ix) % END_INDEX
    return diff >= END_INDEX * FINISH_LINE_ERROR

# old_ix = 250

# went 240 back OR went 260 forward

def passed_checkpoint(kart_id):
    new_item = select_item_for_kart(kart_id)
    event_uid = str(uuid.uuid4())
    logger.info(f"Kart {kart_id} received a {new_item}!")
    send_item(kart_id, new_item, event_uid)

def check_traversed_indices(kart_id, old_index, new_index, current_data):
    traversed = set()
    if new_index < old_index:  # possibly a lap crossing or going backwards
        if check_cross_finish(old_index, new_index):
            current_data["laps"] += 1
            logger.info(f"Kart {kart_id} completed Lap {current_data['laps']}!")
            traversed = set(range(old_index, END_INDEX)) | set(range(0, new_index))
        else:
            logger.debug(f"Kart {kart_id} went backward {old_index - new_index} indices!")
    else:  # moved forward
        traversed = set(range(old_index, new_index))
        logger.debug(f"Kart {kart_id} moved forward {new_index - old_index} indices!")
    
    passed_checkpoints = traversed.intersection(ITEM_INDEX)
    if passed_checkpoints:
        logger.info(f"Kart {kart_id} passed checkpoint(s) at indices: {passed_checkpoints}!")
        passed_checkpoint(kart_id)

def handle_position_estimate(kart_id, loc_index):
    """
    Updates the kart's position and lap count based on new coordinates.
    """
    new_index = loc_index
    current_data = kart_data.get(kart_id)
    if not current_data:
        current_data = {"index": new_index, "laps": 0}
    
    old_index = current_data["index"]
    current_data["index"] = new_index
    
    check_traversed_indices(kart_id, old_index, new_index, current_data)
    
    kart_data[kart_id] = current_data
    update_rankings()

# --- Test Harness ---
def test_handle_position_estimate():
    global kart_data, kart_positions

    # Initialize global state for 3 karts (for example)
    # Let's simulate 3 karts with initial positions.
    kart_data.clear()
    for kart in [1, 2, 3]:
        # For simplicity, let initial index equal y coordinate.
        # We'll give each kart an initial y so that the ranking is 1 > 2 > 3.
        kart_data[kart] = {"index": 0, "laps": 0}
    
    update_rankings()
    logger.info(f"Initial kart_data: {kart_data}")
    logger.info(f"Initial ranking: {kart_positions}")

    # Simulate position updates:
    # For instance, kart 2 is moving forward from index 200 to index 250.
    logger.info("\n--- Test: Kart 2 moves forward ---")
    handle_position_estimate(2, 100)

    # For instance, kart 3 is moving forward from index 200 to index 250.
    logger.info("\n--- Test: Kart 3 moves forward and gets item ---")
    handle_position_estimate(3, 250)

    logger.info("\n--- Test: Kart 2 moves forward and gets item ---")
    handle_position_estimate(2, 450)
    
    # Simulate a lap crossing for kart 2:
    # Suppose the track's END_INDEX is 2000.
    # Kart 2 goes from a high index (e.g., 1900) to a low index (e.g., 100).
    logger.info("\n--- Test: Kart 2 crosses finish line (lap increment) and laps kart 1 ---")
    handle_position_estimate(2, 10)  # Should trigger lap completion

    # Simulate a backward move that is not a lap crossing:
    logger.info("\n--- Test: Kart 3 moves backward without crossing finish ---")
    handle_position_estimate(3, 20)  # Kart 3: from 300 -> 250, not crossing finish line

    # logger.info("\n--- Test: Kart 3 moves crosses finish ---")
    # handle_position_estimate(3, (0, 100))  # Kart 3: from 300 -> 250, not crossing finish line

    # Check final global state.
    logger.info("\nFinal kart_data:")
    for kart, data in kart_data.items():
        logger.info(f"Kart {kart}: {data}")
    logger.info(f"Final ranking: {kart_positions}")

if __name__ == '__main__':
    # Print the current working directory (for debugging purposes)
    import os
    print("Current working directory:", os.getcwd())
    
    test_handle_position_estimate()
