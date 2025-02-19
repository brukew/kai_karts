import struct
from .recieve.position_estimate import update_game
from . import globals
from .recieve.use_item import use_item
import threading
import time

write_lock = threading.Lock()

# Define the magic number (packet start marker)
PACKET_START_MAGIC = 0xDEADBEEF
PACKET_LEN_BYTES = 24

def handle_position_estimate(data):
    ''' 
    Takes in positon estimate from kart and updates game state
    '''
    # print(f"Position Estimate data recieved: {data}")
    globals.GAME_STATE_CHANGED = False
    kart_id = data["from"]
    pos = (data['x'], data['y'])
    loc_index = data["loc_index"]
    event = update_game(kart_id, loc_index, pos)
    if event:
        print("GOT ITEM")
        # uid = globals.get_uid()
        send_item(kart_id, event)
    if globals.GAME_STATE_CHANGED:
        # write_packet(build_get_item_packet())
        write_packet(build_ranking_update_packet(globals.get_kart_positions()))
    return

def handle_use_item(data):
    print(f"Use Item data recieved: {data}")
    kart_id = data['from']
    item = data['item']
    uid = data['uid']
    if uid not in globals.seen_uids:
        print(f"Entering use item logic")
        globals.seen_uids.add(uid)
        victims = use_item(kart_id, item)
        for victim, uid in victims:
            for i in range(10):
                write_packet(build_do_item_packet(victim, item, uid))
    return

def send_item(kart_id, event_uid):
    for i in range(10):
        write_packet(build_get_item_packet(kart_id, event_uid))

def write_packet(packet):
    packet += bytes([0] * (globals.PACKET_LEN_BYTES - len(packet)))
    with write_lock:
        # print("Writing packet twice: ", packet)
        globals.ser.write(packet)
        # globals.ser.write(packet)
        globals.ser.flush()

def build_packet(tag, payload_bytes):
    """Build a complete packet with start magic, tag, and payload."""
    packet = struct.pack('<I', PACKET_START_MAGIC)
    packet += struct.pack('<I', tag)
    packet += payload_bytes
    return packet

def build_ranking_update_packet(positions):
    # tag 4
    # c
    print("Building ranking update packet")
    payload = struct.pack('<' + 'B' * len(positions), *positions)
    return build_packet(4, payload)

def build_do_item_packet(to_val, item, uid):
    # tag 6
    payload = struct.pack('<III', to_val, item, uid)
    return build_packet(6, payload)

def build_get_item_packet(to_val, uid):
    # tag 5
    print("Building get item packet")
    payload = struct.pack('<II', to_val, uid)
    return build_packet(5, payload)
    
def read_packet(executor):
    # look for magic number
    maybe_magic = bytes([0, 0, 0, 0])
    while True:
        read_byte = globals.ser.read(1)
        # print("Reading", read_byte)
        if not read_byte:
            continue
        maybe_magic = maybe_magic[1:] + read_byte
        magic = struct.unpack('<I', maybe_magic)[0]
        if magic == PACKET_START_MAGIC:
            break

    tag_bytes = globals.ser.read(4)
    if len(tag_bytes) < 4:
        return None
    tag = struct.unpack('<I', tag_bytes)[0]

    # print("Tag: ", tag)

    if tag == 2:  # PositionEstimate: { u32 from; u32 x; u32 y; u32 loc_index}
        print("RECIEVED POSITION ESTIMATE")
        payload = globals.ser.read(4 + 4 + 4 + 4)  # 8 bytes total
        # print("Recieving Position Estimate: ", payload)
        if len(payload) < 16:
            return None
        from_val, x, y, loc_index = struct.unpack('<IIII', payload)
        thread = executor.submit(handle_position_estimate, {'from': from_val, 'x': x, 'y': y, 'loc_index': loc_index})
        thread.result()
        return {'tag': 'PositionEstimate', 'from': from_val, 'x': x, 'y': y, 'loc_index': loc_index}
    
    elif tag == 3:  # UseItem: { u32 from; u32 item; u32 uid}
        payload = globals.ser.read(4 + 4 + 4)  # 12 bytes
        print("Recieving Use Item: ", payload)
        if len(payload) < 12:
            return None
        from_val, item, uid= struct.unpack('<III', payload)
        thread = executor.submit(handle_use_item, {'from': from_val, 'item': item, 'uid': uid})
        thread.result()
        return {'tag': 'UseItem', 'from': from_val, 'item': item, 'uid': uid}
    
    else:
        print("Unknown tag:", tag)
        return None
