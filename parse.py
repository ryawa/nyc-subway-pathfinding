import json
import pandas as pd
import networkx as nx

stop_times = pd.read_csv("gtfs/stop_times.txt")
stops = pd.read_csv("gtfs/stops.txt")
transfers = pd.read_csv("gtfs/transfers.txt")
G = nx.DiGraph()

for _, row in stops.iterrows():
    if row["stop_id"][-1] not in ("N", "S"):
        G.add_node(
            row["stop_id"],
            name=row["stop_name"],
            lat=row["stop_lat"],
            lon=row["stop_lon"],
        )


def to_seconds(time):
    h, m, s = [int(part) for part in time.split(":")]
    return 3600 * h + 60 * m + s


skipped = True
for i in range(len(stop_times)):
    if skipped:
        skipped = False

    prev_stop = stop_times.iloc[i - 1]
    curr_stop = stop_times.iloc[i]

    if curr_stop["stop_sequence"] != prev_stop["stop_sequence"] + 1:
        skipped = True
        continue
    # If trip is not on weekdays
    if "Weekday" not in curr_stop["trip_id"] and "L0S1" not in curr_stop["trip_id"]:
        skipped = True
        continue

    depart_time = to_seconds(prev_stop["departure_time"])
    arrive_time = to_seconds(curr_stop["arrival_time"])
    travel_time = arrive_time - depart_time
    route_id = prev_stop["trip_id"].split("_")[-1].split(".")[0]
    G.add_edge(
        prev_stop["stop_id"][:-1],
        curr_stop["stop_id"][:-1],
        weight=travel_time,
        route_id=route_id,
    )

for _, row in transfers.iterrows():
    if row["from_stop_id"] != row["to_stop_id"]:
        G.add_edge(
            row["from_stop_id"],
            row["to_stop_id"],
            weight=row["min_transfer_time"],
            transfer=True,
        )

print(G)

node_link_data = nx.node_link_data(G, edges="edges")
with open("graph.json", "w") as f:
    json.dump(node_link_data, f)

# Weekday only
# Includes all rush hour service
# Slow/parses all trips
# No transfer time at same stop
# overwritten, express, weekday, rush hour, timings
