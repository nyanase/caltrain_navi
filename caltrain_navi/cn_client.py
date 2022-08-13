import googlemaps
from caltrain_navi.caltrain import Train, Station, CaltrainNavi
import re
from datetime import time

class CN_Client:

  def __init__(self, gm_key, trains_path, stations_path) -> None:
    self.gm_key = gm_key
    self.gm_client = self.gmaps_client(self.gm_key)
    self.cnavi = self.init_caltrain_navi(
      trains_path=trains_path, 
      stations_path=stations_path
    )

  def init_caltrain_navi(self, trains_path, stations_path):
    cnavi = CaltrainNavi(trains_path=trains_path, stations_path=stations_path)
    cnavi.load_trains_and_stations()
    return cnavi

  
  def gmaps_client(self, key):
    return googlemaps.Client(key=key)


  def get_closest_times_stations(self, origin, *args, **kwargs):
    destinations = [station.address if station.address != "" \
      else station.coordinates for station in self.cnavi.stations.values()]
    durations = self.get_durations(origin, destinations[:10], *args, **kwargs)
    return sorted(zip(durations, destinations))


  def get_durations(self, *args, **kwargs):
    d_matrix_res = self.distance_matrix_res(*args, **kwargs) 
    return durations_from_d_matrix_res(d_matrix_res)


  def distance_matrix_res(self, *args, **kwargs):
    return self.gm_client.distance_matrix(*args, **kwargs)


def duration_to_time(duration):
  # print(duration)
  regex = r'((?P<hour>\d+) hours? )?(?P<minute>\d+) mins?'
  m = re.match(regex, duration)
  return match_to_time(m)


def match_to_time(m):
  hour, minute = m.group('hour'), m.group('minute')
  hour = to_int_or_zero(hour)
  minute = to_int_or_zero(minute)
  return time(hour=hour, minute=minute)


def to_int_or_zero(str):
  return 0 if str is None else int(str) 


def durations_from_d_matrix_res(d_matrix_res):
  f_durations = []
  for element in d_matrix_res["rows"][0]["elements"]:
    duration = duration_from_element(element)
    f_durations.append(duration_to_time(duration))
  return f_durations


def duration_from_element(element):
  return element["duration"]["text"] 