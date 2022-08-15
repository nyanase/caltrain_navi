from datetime import datetime
from caltrain_navi.cn_client import CN_Client, get_coords_from_str
from caltrain_navi.constants import google_maps_key
cn_client = CN_Client(gm_key=google_maps_key,
                      trains_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json",
                      stations_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json"
            )

dep_time = datetime(2022, 8, 15, 7, 0)
dest_sta = cn_client.cnavi.stations["San Francisco"]
origin = "319 Eleanor Avenue, Los Altos, CA 94022"
mode="bicycling"
res = cn_client.earliest_arrivals(
  dep_time=dep_time,
  dest_sta=dest_sta,
  origin=origin,
  mode=mode,
  num_stations=12
)

for r in res[:9]:
  print(f"current time: {dep_time.time()}")
  print(f"time to {r[2].name} stn: {r[1]}")
  print(f"arrive at {r[2].name} stn at: {(dep_time + r[1]).time()}")
  train = r[3] 
  time_waiting = datetime(1, 1, 1, hour=train.stations[r[2].name].hour,minute=train.stations[r[2].name].minute) - \
    datetime(1, 1, 1, hour=(dep_time + r[1]).hour,minute=(dep_time + r[1]).minute)
  print(f"wait for: {time_waiting.seconds // 3600} hours and {(time_waiting.seconds // 60) % 60} minutes")
  print(f"depart train {train.number} at: {train.stations[r[2].name]}")
  print(f"arrive at {dest_sta.name} stn at: {r[0]}")
  print("\n")