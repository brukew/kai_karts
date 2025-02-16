from server.utils import kart_positions
from .send import send

def update_rank():
    send({"command": 'UPDATE', "args": {"positions": kart_positions}})
    return