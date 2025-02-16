import os
print (os.getcwd())

from ..utils import (
    kart_positions,
    ITEM_INDEX,
    convert_coordinate_to_index,
    select_item_for_kart,
    END_INDEX,
    update_rankings,
    kart_data
)

from logging import getLogger

logger = getLogger()

import uuid
from ..send.send_item import send_item

FINISH_LINE_ERROR = 0.8

def check_cross_finish(old_ix, new_ix) -> bool:
    '''Return True if the difference between old_ix and new_ix indicates a finish-line crossing. Assume indices wrap around at END_INDEX.'''
    # Compute the forward difference on a circular track.
    diff = (old_ix - new_ix) % END_INDEX
    # If diff is close to the full track length (> FINISH_LINE_ERROR% of END_INDEX), consider it a lap crossing.
    return diff >= END_INDEX * FINISH_LINE_ERROR

def passed_checkpoint(kart_id):
    new_item = select_item_for_kart(kart_id)
    event_uid = str(uuid.uuid4())  # unique event identifier
    logger.info(f"Kart {kart_id} recieved a {new_item}!")
    send_item(kart_id, new_item, event_uid)

def check_traversed_indices(kart_id, old_index, new_index, current_data):
    traversed = set()
    # if went backwards - did not traverse any new indices
    if new_index < old_index: # either passed finish line or went backwards
        if check_cross_finish(old_index, new_index):
            current_data["laps"] += 1
            logger.info(f"Kart {kart_id} completed Lap {current_data['laps']}!")
            traversed = set(range(old_index, END_INDEX)) | set(range(0, new_index))
        else:
            logger.debug(f"Kart {kart_id} went backward {old_index-new_index} indices!")
    else: # went forward
        traversed = set(range(old_index, new_index))
        logger.debug(f"Kart {kart_id} went forward {new_index-old_index} indices!")
    
    passed_checkpoints = traversed.intersection(ITEM_INDEX)
    if passed_checkpoints:
        logger.info(f"Kart {kart_id} passed Item Checkpoint at {passed_checkpoints}!")
        passed_checkpoint(kart_id)

def handle_position_estimate(kart_id, loc_index):
    """
    Handles updating position based on new kart positions
    """
    new_index = loc_index
    current_data = kart_data.get(kart_id, None)
    if not current_data:
        current_data = {"index": new_index, "laps": 0}

    old_index = current_data["index"]

    current_data["index"] = new_index

    check_traversed_indices(kart_id, old_index, new_index, current_data)

    kart_data[kart_id] = current_data
    update_rankings()