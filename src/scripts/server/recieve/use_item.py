from server.utils import player_items, ITEM_TARGET, kart_positions, ITEMS
from server.send.apply_item import apply_item
from logging import getLogger

logger = getLogger()

def handle_use_item(kart_id: int, item: int):
    try:
        item_name = ITEMS[item]
    except IndexError:
        logger.warning(f"Use Item: Invalid item index {item} for kart {kart_id}.")
        return

    item_targets = ITEM_TARGET.get(item_name)
    if item_targets is None:
        logger.warning(f"Use Item: No target configuration for item '{item_name}'")
        return

    # Determine victims based on the target type.
    if item_targets == "first":
        # Target the leader.
        victim_ids = [kart_positions[0]] if kart_positions else []
    
    elif item_targets == "all":
        # Target every kart except the one using the item.
        victim_ids = kart_positions.copy()
        if kart_id in victim_ids:
            victim_ids.remove(kart_id)
    
    elif isinstance(item_targets, list):
        try:
            kart_ix = kart_positions.index(kart_id)
        except ValueError:
            logger.warning(f"Use Item: Kart ID {kart_id} not found in ranking.")
            return
        
        # Compute absolute target indices.
        victim_ix = [kart_ix - target for target in item_targets]
        # Ensure indices are within bounds of kart_positions.
        victim_ids = [
            kart_positions[ix]
            for ix in victim_ix
            if ix >= 0 and ix < len(kart_positions)
        ]
    else:
        logger.warning(f"Use Item: Unexpected target type for item '{item_name}': {item_targets}")
        return

    apply_item(kart_id, item, victim_ids)

