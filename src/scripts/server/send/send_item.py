from .send import send

from logging import getLogger

logger = getLogger()

def send_item(kart_id, item, event_uid):
    """
    Send an item to a kart.
    """
    logger.info(f"Sending item {item} to kart {kart_id} with event_uid {event_uid}")
    send({"command": "ITEM", "args":{"kart_id": kart_id, "item": item, "uid": event_uid}})
    return