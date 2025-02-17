import struct
from logging import getLogger
from .recieve.position_estimate import update_game
import utils
import globals
from .recieve.use_item import use_item

# Define the magic number (packet start marker)
PACKET_START_MAGIC = 0xDEADBEEF

logger = getLogger("SerialReader")

def handle_position_estimate(data):
    ''' 
    Takes in positon estimate from kart and updates game state
    '''
    print("PositionEstimate:", data)
    kart_id = data["from"]
    loc_index = data["loc_index"]
    track_id = data["track_id"]
    update_game(kart_id, loc_index, track_id)
    write_packet(build_ranking_update_packet(globals.kart_positions))
    return

def handle_use_item(data):
    print("UseItem:", data)
    kart_id = data['from']
    item = data['item']
    uid = data['uid']
    if uid not in utils.seen_uids:
        utils.seen_uids.add(uid)
        victims = use_item(kart_id, item)
        for victim, uid in victims:
            write_packet(build_do_item_packet(victim, item, uid))
    return

def write_packet(packet):
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

def read_packet():
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

    if tag == 2:  # PositionEstimate: { u32 from; i32 loc_index; u32 track_id }
        payload = globals.ser.read(4 + 4 + 4)  # 12 bytes total
        if len(payload) < 12:
            return None
        from_val, loc_index, track_id = struct.unpack('<IiI', payload)
        handle_position_estimate({'from': from_val, 'loc_index': loc_index, 'track_id': track_id})
        return {'tag': 'PositionEstimate', 'from': from_val, 'loc_index': loc_index}
    
    elif tag == 3:  # UseItem: { u32 from; u32 item; u32 uid}
        payload = globals.ser.read(4 + 4 + 4)  # 12 bytes
        if len(payload) < 12:
            return None
        from_val, item, uid= struct.unpack('<III', payload)
        handle_use_item({'from': from_val, 'item': item, 'uid': uid})
        return {'tag': 'UseItem', 'from': from_val, 'item': item, 'uid': uid}
    
    else:
        print("Unknown tag:", tag)
        return None
