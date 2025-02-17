from collections import defaultdict
import globals

def convert_coordinate_to_index(x: int, y: int) -> int:
    return y #Placeholder for testing

def select_item_for_kart(rank: int) -> str:
    return

def update_rankings():
    new_rank = list(globals.kart_data.keys())
    new_rank.sort(key = lambda x: (kart_data[x]["laps"], kart_data[x]["index"]), reverse = True)
    globals.kart_positions = new_rank