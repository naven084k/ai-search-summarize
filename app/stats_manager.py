import json
import os

STATS_FILE = "data/stats.json"

# Initialize stats file if missing
def init_stats():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.isfile(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            json.dump({"uploads": 0, "queries": 0}, f)

def read_stats():
    init_stats()
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def increment_stat(key):
    stats = read_stats()
    stats[key] = stats.get(key, 0) + 1
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)
