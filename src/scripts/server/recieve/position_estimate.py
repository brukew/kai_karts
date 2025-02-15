import os
print (os.getcwd())

from ..utils import (
    kart_positions,
    ITEM_INDEX,
    convert_coordinate_to_index,
    select_item_for_kart,
    player_items,
    END_INDEX,
    update_ranking,
)

import uuid
from ..send import send_item

MIN_DIFF_NOISE = END_INDEX - END_INDEX*0.1

def check_cross_finish(old_ix, new_ix) -> bool:
    ''' Logic to check if kart passed finish line vs. went backwards
        1098 -> 5
        vs 
        5 -> 0

        need to account for 5 -> 1098 then 1098 -> 5 (should not count as another lap)
    '''
    # TODO: Revise for correctness and robustness against hacking (going back and forth between finish line)
    if new_ix > old_ix:
        return False

    return old_ix - new_ix >= MIN_DIFF_NOISE

def handle_position_estimate(kart_id, pos):
    """
    
    """
    x, y = pos
    track_index = convert_coordinate_to_index(x, y)
    current_data = kart_positions.get(kart_id, {"index": 0, "laps": 0, "position": (0,0)})
    old_index = current_data["index"]

    #TODO: verify location 

    current_data["index"] = track_index
    current_data["position"] = (x, y)

    if track_index < old_index: # either passed finish line or went backwards
        if check_cross_finish(old_index, track_index):
            current_data["laps"] += 1
            print(f"Kart {kart_id} completed lap {current_data['laps']}")

    traversed = {i for i in range(old_index, track_index)}
    #TODO: fix this logic if track_index is < old_index b/c it went backwards or /c it crossed finish line
    
    if traversed.intersection(ITEM_INDEX):
        new_item = select_item_for_kart(kart_id)
        # Store item in player_items
        event_uid = str(uuid.uuid4())  # unique event identifier
        player_items[kart_id] = new_item
        # Possibly send "Send Item" message to that kart
        send_item(kart_id, new_item, event_uid)

    kart_positions[kart_id] = current_data
    update_ranking()

    # logger()
    # log_action("PositionEstimate", {"kart_id": kart_id, "position": (x, y), "index": track_index})
