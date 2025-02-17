from .send import send

from logging import getLogger

logger = getLogger()

import uuid

def apply_item(kart_id, item, victims):
    events = []
    for victim_kart_id in victims:
        event_uid = str(uuid.uuid4())  # unique event for buff/debuff
        events.append((victim_kart_id, event_uid))
        logger.info(f"Kart {kart_id} applied {item} to kart {victim_kart_id} with event_uid {event_uid}")
    return events