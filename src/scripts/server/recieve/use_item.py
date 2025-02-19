from .. import globals
from server.send.apply_item import apply_item

def use_item(kart_id: int, item: int) -> list:
    '''
    Determines kart id of all victims based on item.

    Returns list containing (victim_id, event_id) for each victim
    '''
    try:
        item_name = globals.ITEMS[item]
    except IndexError:
        print(f"Use Item: Invalid item index {item} for kart {kart_id}.")
        return

    item_targets = globals.ITEM_TARGET.get(item_name)
    print(f"Item targets: {item_targets}")
    if item_targets is None:
        print(f"Use Item: No target configuration for item '{item_name}'")
        return

    # Determine victims based on the target type.
    if item_targets == "first":
        # Target the leader.
        victim_ids = [globals.get_kart_positions()[0]] if globals.get_kart_positions() else []
    
    elif item_targets == "all":
        # Target every kart except the one using the item.
        victim_ids = globals.get_kart_positions().copy()
        if kart_id in victim_ids:
            victim_ids.remove(kart_id)
    
    elif isinstance(item_targets, list):
        try:
            kart_ix = globals.get_kart_positions().index(kart_id)
        except ValueError:
            print(f"Use Item: Kart ID {kart_id} not found in ranking.")
            return
        
        # Compute absolute target indices. (subtraction because ordered list is descending position)
        victim_ix = [kart_ix - target for target in item_targets]
        # Ensure indices are within bounds of kart_positions.
        victim_ids = [
            globals.get_kart_positions()[ix]
            for ix in victim_ix
            if ix >= 0 and ix < len(globals.get_kart_positions())
        ]
    else:
        print(f"Use Item: Unexpected target type for item '{item_name}': {item_targets}")
        return []

    return apply_item(kart_id, item, victim_ids)

