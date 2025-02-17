from collections import defaultdict
import globals

def update_rankings():
    globals.kart_positions = sorted(globals.kart_data.keys(), key=lambda k: (globals.kart_data[k]["laps"], globals.kart_data[k]["index"]), reverse=True)