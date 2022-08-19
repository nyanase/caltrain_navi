from datetime import datetime
from caltrain_navi.cn_client import CN_Client, get_coords_from_str
from caltrain_navi.constants import google_maps_key
cn_client = CN_Client(gm_key=google_maps_key,
                      trains_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json",
                      stations_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json"
            )

# dep_time = datetime(2022, 8, 15, 7, 0)
dep_time = datetime.now()
dest_sta = cn_client.cnavi.stations["San Francisco"]
origin = "319 Eleanor Avenue, Los Altos, CA 94022"
mode="bicycling"
res = cn_client.earliest_arrivals(
  dep_time=dep_time,
  dest_sta=dest_sta,
  origin=origin,
  mode=mode,
  num_stations=4
)

for r in res[:9]:
  print(r)
  print("\n")