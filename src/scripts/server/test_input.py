import threading
from .serial_read import build_ranking_update_packet, build_get_item_packet, build_do_item_packet, write_packet
import logging
from .globals import get_kart_positions, ITEMS

logger = logging.getLogger("SerialReader").setLevel(logging.INFO)

def run_ranking_update(*args):
    print("Ranking update command received.")
    packet = build_ranking_update_packet(get_kart_positions())
    write_packet(packet)

def run_get_item(*args):
    # Example: args[0] is kart_id, args[1] is event_uid
    print("Get item command received.")
    if len(args) < 2:
        print("Usage: get_item <kart_id> <event_uid>")
        return
    kart_id, event_uid = args[0], args[1]
    packet = build_get_item_packet(int(kart_id), int(event_uid))
    write_packet(packet)

def run_do_item(*args):
    # Example: args[0] is kart_id, args[1] is item, args[2] is uid
    print("Do item command received.")
    if len(args) < 3:
        print("Usage: do_item <kart_id> <item> <uid>")
        return
    kart_id, item, uid = args[0], args[1], args[2]
    print(f"Kart {kart_id} using or hit with item {ITEMS[int(item)]} with event_uid {uid}")
    packet = build_do_item_packet(int(kart_id), int(item), int(uid))
    write_packet(packet)

def command_input_loop(executor):
    print("Command input thread started. Enter commands (e.g., ranking_update, get_item, do_item):")
    while True:
        try:
            # This input call is blocking, but that's fine in its own thread.
            command_line = input("> ")
            if not command_line:
                continue
            parts = command_line.split()
            command = parts[0]
            args = parts[1:]
            
            if command == "ru":
                # Submit ranking update to the executor.
                print("yer")
                # thread = executor.submit(run_ranking_update, *args)
                # thread.result()
                run_ranking_update()
            elif command == "gi":
                thread = executor.submit(run_get_item, *args)
                thread.result()
            elif command == "dei":
                thread = executor.submit(run_do_item, *args)
                thread.result()
            else:
                print("Unknown command. Valid commands: ranking_update, get_item, do_item")
        except Exception as e:
            print("Error processing command:", e)

def input_init(executor):
    # Start the command input loop in its own thread.
    command_thread = threading.Thread(target=command_input_loop, args = (executor, ), daemon=True)
    command_thread.start()
