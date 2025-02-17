import struct
from logging import getLogger
from .recieve.position_estimate import update_game
import globals
from .recieve.use_item import use_item
import threading

write_lock = threading.Lock()

# Define the magic number (packet start marker)
PACKET_START_MAGIC = 0xDEADBEEF
PACKET_LEN_BYTES = 24

logger = getLogger("SerialReader")

def handle_position_estimate(data):
    ''' 
    Takes in positon estimate from kart and updates game state
    '''
    logger.info(f"Position Estimate data recieved: {data}")
    kart_id = data["from"]
    x = data['x']
    y = data['y']
    pos = (data['x'], data['y'])
    loc_index = data["loc_index"]
    update_game(kart_id, loc_index, pos)
    write_packet(build_ranking_update_packet(globals.get_kart_positions()))
    return

def handle_use_item(data):
    logger.info(f"Use Item data recieved: {data}")
    kart_id = data['from']
    item = data['item']
    uid = data['uid']
    if uid not in globals.seen_uids:
        globals.seen_uids.add(uid)
        victims = use_item(kart_id, item)
        for victim, uid in victims:
            write_packet(build_do_item_packet(victim, item, uid))
    return

def send_item(kart_id, event_uid):
    write_packet(build_get_item_packet(kart_id, event_uid))

def write_packet(packet):
    packet += bytes([0] * (globals.PACKET_LEN_BYTES - len(packet)))
    with write_lock:
        globals.ser.write(packet)

def build_packet(tag, payload_bytes):
    """Build a complete packet with start magic, tag, and payload."""
    packet = struct.pack('<I', PACKET_START_MAGIC)
    packet += struct.pack('<I', tag)
    packet += payload_bytes
    return packet

def build_ranking_update_packet(positions):
    # tag 4
    payload = struct.pack('<' + 'B' * len(positions), *positions)
    return build_packet(4, payload)

def build_do_item_packet(to_val, item, uid):
    # tag 6
    payload = struct.pack('<III', to_val, item, uid)
    return build_packet(6, payload)

def build_get_item_packet(to_val, uid):
    # tag 5
    payload = struct.pack('<II', to_val, uid)
    return build_packet(5, payload)
    
def read_packet(executor):
    # look for magic number
    maybe_magic = bytes([0, 0, 0, 0])
    while True:
        maybe_magic = maybe_magic[1:] + globals.ser.read(1)
        magic = struct.unpack('<I', maybe_magic)[0]
        if magic == PACKET_START_MAGIC:
            break  # found the packet start

    tag_bytes = globals.ser.read(4)
    if len(tag_bytes) < 4:
        return None
    tag = struct.unpack('<I', tag_bytes)[0]

    if tag == 2:  # PositionEstimate: { u32 from; u32 x; u32 y; u32 loc_index}
        payload = globals.ser.read(4 + 4)  # 8 bytes total
        if len(payload) < 8:
            return None
        from_val, x, y, loc_index = struct.unpack('<IIII', payload)
        executor.submit(handle_position_estimate, {'from': from_val, 'x': x, 'y': y, 'loc_index': loc_index})
        return {'tag': 'PositionEstimate', 'from': from_val, 'x': x, 'y': y, 'loc_index': loc_index}
    
    elif tag == 3:  # UseItem: { u32 from; u32 item; u32 uid}
        payload = globals.ser.read(4 + 4 + 4)  # 12 bytes
        if len(payload) < 12:
            return None
        from_val, item, uid= struct.unpack('<III', payload)
        executor.submit(handle_use_item, {'from': from_val, 'item': item, 'uid': uid})
        return {'tag': 'UseItem', 'from': from_val, 'item': item, 'uid': uid}
    
    else:
        print("Unknown tag:", tag)
        return None
