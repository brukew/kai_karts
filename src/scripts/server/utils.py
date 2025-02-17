from collections import defaultdict
import globals

def update_rankings():
    globals.update_kart_positions(sorted(globals.get_kart_data().keys(), key=lambda k: (globals.get_kart_data()[k]["laps"], globals.get_kart_data()[k]["index"]), reverse=True))