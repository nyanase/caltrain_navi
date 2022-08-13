import pytest
from caltrain_navi.cn_client import CN_Client
from datetime import time
from caltrain_navi.constants import google_maps_key


cn_client = CN_Client(google_maps_key,
                      trains_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json",
                      stations_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json")

def test_get_duration():
  durations = cn_client.get_durations(origins=["319 Eleanor Ave, Los Altos, CA 94022"],
    destinations=["600 W Evelyn Ave, Mountain View, CA 94041", "95 University Ave, Palo Alto, CA 94301", "37.62975157426811, -122.41133366960393"], 
    mode="bicycling"
  )
  # assert durations == ["14 mins", "33 mins", "2 hours 21 mins"]
  assert durations == [time(0, 14), time(0, 33), time(2, 21)]
  