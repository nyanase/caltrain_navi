from collections import defaultdict
import googlemaps
from caltrain_navi.caltrain import CaltrainNavi
from caltrain_navi.utils import duration_to_time, duration_from_element, \
  get_coords_from_str

class CN_Client:

  def __init__(self, gm_key, trains_path, stations_path) -> None:
    self.gm_key = gm_key
    self.gm_client = self.init_gmaps_client(self.gm_key)
    self.cnavi = self.init_caltrain_navi(
      trains_path=trains_path, 
      stations_path=stations_path
    )


  def init_caltrain_navi(self, trains_path, stations_path):
    cnavi = CaltrainNavi(trains_path=trains_path, stations_path=stations_path)
    cnavi.load_trains_and_stations()
    return cnavi

  
  def init_gmaps_client(self, key):
    return googlemaps.Client(key=key)
  
  
  def earliest_arrivals(self, dep_time, dest_sta, 
                        origin, *args, num_stations=3,
                        max_trains=3, **kwargs):
    ttstns_stns = self.ttstns_stns_to_closest_stns(
      origin, num_stations, *args, **kwargs)
    arrivals_res = []
    for ttstn, stn in ttstns_stns:
      stn_dep_time = dep_time + ttstn 
      for arrv_time, train in self.cnavi.earliest_arrival_times(
        stn_dep_time, stn, dest_sta, max_trains 
      ):
        arrivals_res.append((arrv_time, ttstn, stn, train))
    return sorted(arrivals_res, key=lambda k: k[0])

  
  def ttstns_stns_to_closest_stns(
    self, origin, num_stations=6, *args, **kwargs):
    closest_sts = self.get_closest_stations(origin, num_stations) 
    cl_sts_locs = [self.station_loc(station) for station in closest_sts]
    durations = self.get_durations(origin, cl_sts_locs, *args, **kwargs)
    return sorted(zip(durations, closest_sts), key=lambda k: k[0])


  def get_closest_stations(self, origin, num_stations=6):
    origin = self.format_origin(origin)
    return self.get_closest_stations_formatted_origin(
      origin, num_stations=num_stations)


  def format_origin(self, origin):
    if isinstance(origin, str):
      coords = get_coords_from_str(origin)
      return coords if coords else self.get_coords_from_address(origin)
    return origin
  
  
  def get_coords_from_address(self, address):
    geocode_res = self.geocode(address)
    if len(geocode_res) == 0: 
      raise Exception("Failed to geocode address")
    return self.get_coords_from_geocode_res(geocode_res)


  def get_coords_from_geocode_res(self, geocode_res):
    location = geocode_res[0]["geometry"]["location"]
    return location["lat"], location["lng"]
  

  def geocode(self, address):
    return self.gm_client.geocode(address)


  def get_closest_stations_formatted_origin(self, origin, num_stations=6):
    distances_stations = [(station.distance_to(origin), station) for station in \
      self.cnavi.stations.values()]
    sorted_stations =  sorted(distances_stations, key=lambda k: k[0])[:num_stations]
    return [s[1] for s in sorted_stations]


  def get_durations(self, *args, **kwargs):
    d_matrix_res = self.distance_matrix_res(*args, **kwargs) 
    return self.durations_from_d_matrix_res(d_matrix_res)


  def distance_matrix_res(self, *args, **kwargs):
    return self.gm_client.distance_matrix(*args, **kwargs)


  def durations_from_d_matrix_res(self, d_matrix_res):
    f_durations = []
    for element in d_matrix_res["rows"][0]["elements"]:
      duration = duration_from_element(element)
      f_durations.append(duration_to_time(duration))
    return f_durations


  def station_loc(self, station):
    return station.address if station.address != "" else station.coordinates