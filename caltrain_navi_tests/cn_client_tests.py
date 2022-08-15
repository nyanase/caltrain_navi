import pytest
from caltrain_navi.cn_client import CN_Client
from datetime import time, timedelta
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
  assert durations == [timedelta(minutes=14), timedelta(minutes=33), 
                       timedelta(hours=2, minutes=21)]
  
def test_format_origin():
  assert cn_client.format_origin("37.37687798746064, -122.10947593981749") == \
    (37.37687798746064, -122.10947593981749)

  assert cn_client.format_origin("(37.37687798746064, -122.10947593981749)") == \
    (37.37687798746064, -122.10947593981749)
  
  assert cn_client.format_origin("319 Eleanor Avenue, Los Altos, CA 94022") == \
    (37.3768696, -122.1095064) 
  
def test_ttstns_stns_to_closest_stns():
  ttstns_stns = cn_client.ttstns_stns_to_closest_stns(
    "319 Eleanor Avenue, Los Altos, CA 94022",
    num_stations=3,
    mode="bicycling",
  )
  assert ttstns_stns == [
    (timedelta(minutes=13), cn_client.cnavi.stations["San Antonio"]),
    (timedelta(minutes=14), cn_client.cnavi.stations["Mountain View"]),
    (timedelta(minutes=24), cn_client.cnavi.stations["California Avenue"]),
  ]

  ttstns_stns = cn_client.ttstns_stns_to_closest_stns(
    "37.37687798746064, -122.10947593981749",
    num_stations=3,
    mode="bicycling",
  )
  assert ttstns_stns == [
    (timedelta(minutes=13), cn_client.cnavi.stations["San Antonio"]),
    (timedelta(minutes=14), cn_client.cnavi.stations["Mountain View"]),
    (timedelta(minutes=24), cn_client.cnavi.stations["California Avenue"]),
  ]
  
  