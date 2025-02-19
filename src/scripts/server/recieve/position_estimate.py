import os
print (os.getcwd())

from ..utils import (
    update_rankings,
)

from .. import globals

import threading

lock = threading.Lock()

FINISH_LINE_ERROR = 0.8

MAX_DIST_TRAVELLED = 0.8 * globals.END_INDEX

def check_cross_finish(old_ix, new_ix) -> bool:
    '''Return True if the difference between old_ix and new_ix indicates a finish-line crossing. Assume indices wrap around at END_INDEX.'''
    diff = (old_ix - new_ix) % globals.END_INDEX
    # If diff is close to the full track length (> FINISH_LINE_ERROR% of END_INDEX), consider it a lap crossing.
    return diff >= globals.END_INDEX * FINISH_LINE_ERROR

def check_traversed_indices(kart_id, old_index, new_index, current_data):
    # collects traversed indices
    traversed = set()
    if new_index < old_index: # if went backwards - it either passed finish line or went just drove backwards
        if check_cross_finish(old_index, new_index):
            # update laps
            current_data["laps"] += 1
            # print(f"Kart {kart_id} completed Lap {current_data['laps']}!")
            traversed = set(range(old_index, globals.END_INDEX)) | set(range(0, new_index))
        else:
            # print(f"Kart {kart_id} went backward {old_index-new_index} indices!")
            pass
    else: # went forward
        traversed = set(range(old_index, new_index))
        # print(f"Kart {kart_id} went forward {new_index-old_index} indices!")

    return traversed

def update_game(kart_id, loc_index, pos): # TODO: deal with pos
    """
    Handles updating position based on new kart positions
    """
    # print("Updating game state for kart", kart_id, "to index", loc_index)
    new_index = loc_index
    new_pos = pos
    current_data = globals.get_kart_data().get(kart_id, None)
    # if kart is new, initialize data
    if not current_data:
        current_data = {"index": new_index, "laps": 0, "pos": new_pos}
    old_index = current_data["index"]
    # old_pos = current_data["pos"]
    current_data["index"] = new_index
    current_data["pos"] = pos

    if abs(new_index - old_index) > MAX_DIST_TRAVELLED: 
        return None


    # collect traversed indices and check if kart passed finish line
    traversed = check_traversed_indices(kart_id, old_index, new_index, current_data)

    checkpoint = False
    # check if kart passed any item checkpoints
    passed_checkpoints = traversed.intersection(globals.ITEM_INDEX)
    if passed_checkpoints:
        # check if kart passed the multi-path checkpoint
        if len(passed_checkpoints) == 1 and globals.multi_path_checkpoint["index"] in passed_checkpoints:
            if pos in globals.multi_path_checkpoint["points"]:
                pass
                # print(f"Kart {kart_id} passed Multi-Path Checkpoint at {passed_checkpoints} and recieved an item!")
        else:
            # print(f"Kart {kart_id} passed Item Checkpoint at {passed_checkpoints} and recieved an item!")
            pass
        event_uid = globals.get_uid()
        checkpoint = True
    else:
        pass
        # print("Kart passed no checkpoints")

    globals.update_kart_data(kart_id, current_data)
    update_rankings()

    return event_uid if checkpoint else None