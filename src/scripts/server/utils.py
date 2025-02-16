import uuid
import time
from collections import defaultdict

# Internal Ranking
#    We'll keep a dict {kart_id: {"index": track_index, "laps": int}}
#    Then, on each update, we recompute an ordered list for who is leading.
kart_data = {}
kart_positions = []

# Items
ITEMS = ["banana", "bob-omb", "red_shroom", "lightning", "bullet_bill", "gold_shroom", "red_shell", "blue_shell"]

#   A dict that maps item names to their targets relative to the player that used it
ITEM_TARGET = {
    "banana": {"target":[-1]}, # 0% chance for last
    "bob-omb": {"target":[1, 2, 3]}, # 0% chance for first
    "red_shroom": {"target":[0]},
    "lightning": {"target":"all"},
    "bullet_bill": {"target":[0]},
    "gold_shroom": {"target":[0]}, 
    "red_shell": {"target":[1]}, # 0% chance for first
    "blue_shell": {"target":"first"}
}

# Player -> Items (inventory or current item)
#    A dict of lists or single slots, depending on your design.
# player_items = defaultdict(str)  # e.g. player_items[kart_id] = ["banana"]



# Item Weights (based on rank)
ITEM_WEIGHTS = {
    # Rank 1 (Leader): Defensive items only; no powerful items.
    1: {
        "banana": 0.5,       # high chance for banana (defensive)
        "bob-omb": 0.0,      # no bombs
        "red_shroom": 0.2,   # moderate chance for a boost item (if used defensively)
        "lightning": 0.0,    # no lightning
        "bullet_bill": 0.0,  # no bullet bill
        "gold_shroom": 0.0,  # no gold shroom
        "red_shell": 0.3,    # chance for red shell (to deter attackers from behind)
        "blue_shell": 0.0    # no blue shell for leader
    },
    # Rank 2: Still mostly defensive; very low chance for any offensive bomb.
    2: {
        "banana": 0.3,
        "bob-omb": 0.05,
        "red_shroom": 0.2,
        "lightning": 0.0,
        "bullet_bill": 0.0,
        "gold_shroom": 0.05,
        "red_shell": 0.4,
        "blue_shell": 0.0
    },
    # Rank 3: A mix begins—some chance for offensive items.
    3: {
        "banana": 0.1,
        "bob-omb": 0.1,
        "red_shroom": 0.2,
        "lightning": 0.0,
        "bullet_bill": 0.1,
        "gold_shroom": 0.1,
        "red_shell": 0.3,
        "blue_shell": 0.1
    },
    # Rank 4: Lower-ranked; moderate chance for offensive items.
    4: {
        "banana": 0.05,
        "bob-omb": 0.1,
        "red_shroom": 0.1,
        "lightning": 0.1,
        "bullet_bill": 0.15,
        "gold_shroom": 0.1,
        "red_shell": 0.2,
        "blue_shell": 0.2
    },
    # Rank 5: Even lower; increased chance for powerful items.
    5: {
        "banana": 0.05,
        "bob-omb": 0.05,
        "red_shroom": 0.1,
        "lightning": 0.15,
        "bullet_bill": 0.2,
        "gold_shroom": 0.1,
        "red_shell": 0.15,
        "blue_shell": 0.2
    },
    # Rank 6 (Last): Highest chance for powerful, offensive items.
    6: {
        "banana": 0.01,
        "bob-omb": 0.05,
        "red_shroom": 0.1,
        "lightning": 0.2,
        "bullet_bill": 0.25,
        "gold_shroom": 0.1,
        "red_shell": 0.15,
        "blue_shell": 0.14
    },
    # Default: Used if a player's rank doesn't fall into 1-6.
    "default": {
        "banana": 0.05,
        "bob-omb": 0.05,
        "red_shroom": 0.1,
        "lightning": 0.15,
        "bullet_bill": 0.15,
        "gold_shroom": 0.1,
        "red_shell": 0.2,
        "blue_shell": 0.2
    }
}

# TODO: Coordinate to Index
#    Mapping from (x,y) or a grid region to a "track_index."
#    For simplicity, let’s say we store boundaries for each index.
COORDINATE_TO_INDEX = [
    # e.g., [ {"index": 0, "xrange": (0,10), "yrange": (0,5)}, ... ]
]

# TODO:Item Index 
#    The list of track indices that award an item
ITEM_INDEX = {10, 25, 50}  # example track positions

# TODO: Finish Line Index
END_INDEX = 2000  # track position that indicates a lap crossing


def convert_coordinate_to_index(x: int, y: int) -> int:
    return y #Placeholder for testing

def select_item_for_kart(rank: int) -> str:
    return

def update_rankings():
    global kart_positions
    new_rank = list(kart_data.keys())
    new_rank.sort(key = lambda x: (kart_data[x]["laps"], kart_data[x]["index"]), reverse = True)
    kart_positions = new_rank