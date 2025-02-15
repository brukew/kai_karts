from ..utils import player_items, ITEM_TARGET, kart_positions
from ..send import apply_item
def handle_use_item(kart_id):
    if player_items["kart_id"]:
        item = player_items["kart_id"]
        item_targets = ITEM_TARGET[item]
        if item_targets == "first":
            victim_ids = [kart_positions[0]]
        elif item_targets == "all":
            victim_ids = kart_positions.copy()
            victim_ids.remove(kart_id)
        elif type(item_targets)==list:
            kart_ix = kart_positions.index(kart_id) + target
            victim_ix = [kart_ix + target for target in item_targets]
            victim_ids = [kart_positions[ix] for ix in victim_ix if ix>0 and ix<len(item_targets)]
        send.apply_item(item, victim_ids)
