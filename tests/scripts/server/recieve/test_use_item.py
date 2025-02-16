# test_use_item_new.py

# --- Global State Definitions (simulate server/utils.py) ---
import sys
from collections import defaultdict

# Ranking of karts: leader is at index 0.
kart_positions = [1, 2, 3, 4, 5, 6]

# List of available items (indexed by integer).
ITEMS = [
    "banana", "bob-omb", "red_shroom", "lightning",
    "bullet_bill", "gold_shroom", "red_shell", "blue_shell"
]

# ITEM_TARGET maps each item name to its targeting configuration.
ITEM_TARGET = {
    "banana": [-1],         # Targets 1 behind.
    "bob-omb": [1, 2, 3],     # Targets 1 to 3 ahead.
    "red_shroom": [0],        # Targets self (e.g., for boost).
    "lightning": "all",       # Targets all other karts.
    "bullet_bill": [0],       # Targets self.
    "gold_shroom": [0],       # Targets self.
    "red_shell": [1],         # Targets immediately ahead.
    "blue_shell": "first"     # Always targets the leader.
}

# --- Test Version of apply_item (simulate server.send.apply_item.apply_item) ---
def test_apply_item(user_kart, item, victim_ids):
    print(f"apply_item called: Kart {user_kart} uses '{ITEMS[item]}' on victims: {victim_ids}")

# --- The use_item logic (simulate use_item.py) ---
def handle_use_item(kart_id: int, item: int):
    """
    Process a use-item command for the given kart.
    'item' is an integer index into ITEMS.
    """
    # Validate the item index.
    try:
        item_name = ITEMS[item]
    except IndexError:
        print(f"Invalid item index {item} for kart {kart_id}.")
        return

    # Get the targeting configuration.
    item_targets = ITEM_TARGET.get(item_name)
    if item_targets is None:
        print(f"No target configuration for item '{item_name}'.")
        return

    # Determine victim IDs based on target configuration.
    if item_targets == "first":
        # Target the leader.
        victim_ids = [kart_positions[0]] if kart_positions else []
    
    elif item_targets == "all":
        # Target all karts except the user.
        victim_ids = kart_positions.copy()
        if kart_id in victim_ids:
            victim_ids.remove(kart_id)
    
    elif isinstance(item_targets, list):
        # Determine the index of the current kart in the ranking.
        try:
            kart_ix = kart_positions.index(kart_id)
        except ValueError:
            print(f"Kart {kart_id} not found in ranking.")
            return
        
        # Compute target indices by adding each offset.
        victim_ix = [kart_ix - target for target in item_targets]
        # Make sure each computed index is within bounds of kart_positions.
        victim_ids = [
            kart_positions[ix]
            for ix in victim_ix
            if ix >= 0 and ix < len(kart_positions)
        ]
    else:
        print(f"Unexpected target configuration for item '{item_name}': {item_targets}")
        return

    # Use our test version of apply_item to simulate applying the item.
    test_apply_item(kart_id, item, victim_ids)

# --- Test Function ---
def test_use_item_new():
    global kart_positions, ITEMS, ITEM_TARGET

    # For testing, we assume kart_positions is already defined.
    # Print the initial ranking.
    print("Initial ranking (kart_positions):", kart_positions)

    # Test Case 1: Kart 3 uses a blue_shell.
    # blue_shell (index 7) targets "first" so expected victim is the leader (kart 1).
    print("\nTest Case 1: Kart 3 uses blue_shell (item index 7)")
    handle_use_item(3, 7)

    # Test Case 2: Kart 4 uses bob-omb.
    # bob-omb (index 1) targets [1, 2, 3].
    # For kart 4, its index in kart_positions is 3 (0-based).
    # Expected victim indices: [3+1, 3+2, 3+3] => [4, 5, 6].
    # However, since there are only 6 karts (indices 0-5), index 6 is out of range.
    # So expected victims: [kart_positions[4], kart_positions[5]] => [5, 6].
    print("\nTest Case 2: Kart 4 uses bob-omb (item index 1)")
    handle_use_item(4, 1)

    # Test Case 3: Kart 2 uses lightning.
    # lightning (index 3) targets "all" so all karts except kart 2 should be victims.
    print("\nTest Case 3: Kart 2 uses lightning (item index 3)")
    handle_use_item(2, 3)

    # Test Case 4: Kart 2 uses lightning.
    # lightning (index 3) targets "all" so all karts except kart 2 should be victims.
    print("\nTest Case 3: Kart 5 uses banana (item index 0)")
    handle_use_item(5, 0)

    # Test Case 5: Kart 2 uses lightning.
    # lightning (index 3) targets "all" so all karts except kart 2 should be victims.
    print("\nTest Case 3: Kart 5 uses red shell (item index 0)")
    handle_use_item(5, 6)

    # Test Case 6: Kart 1 uses red shroom.
    # lightning (index 3) targets "all" so all karts except kart 2 should be victims.
    print("\nTest Case 3: Kart 1 uses red shroom (item index 2)")
    handle_use_item(1, 2)

if __name__ == '__main__':
    test_use_item_new()
