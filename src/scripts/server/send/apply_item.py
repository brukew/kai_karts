from .. import globals

def apply_item(kart_id, item, victims):
    events = []
    print(f"Applying item {item} to {victims}")
    for victim_kart_id in victims:
        event_uid = globals.get_uid()  # unique event for buff/debuff
        events.append((victim_kart_id, event_uid))
        print(f"Kart {kart_id} applied {item} to kart {victim_kart_id} with event_uid {event_uid}")
    return events