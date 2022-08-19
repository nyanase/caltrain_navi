from collections import defaultdict
from dataclasses import dataclass
import googlemaps
from caltrain_navi.caltrain import CaltrainNavi, Station, Train
from caltrain_navi.utils import duration_to_time, duration_from_element, \
  get_coords_from_str, drop_mins_secs
from datetime import datetime, time, timedelta
from inspect import cleandoc

@dataclass
class CalTrainNaviRes:

  arrival_time: time
  time_to_stn: timedelta
  dep_stn: Station
  train: Train
  dep_time: datetime
  dest_stn: Station


  def dep_stn_arrival_time(self):
    return (self.dep_time + self.time_to_stn).time()    


  def time_waiting_for_train(self):
    dep_stn_arrv_time = datetime(1, 1, 1, 
          hour=(self.dep_time + self.time_to_stn).hour,
          minute=(self.dep_time + self.time_to_stn).minute
    )
    dep_stn_dep_time = datetime(1, 1, 1, 
          hour=self.train.stations[self.dep_stn.name].hour, 
          minute=self.train.stations[self.dep_stn.name].minute
    ) 
    return dep_stn_dep_time - dep_stn_arrv_time
  
  
  def time_on_train(self):
    leave_time = datetime(1, 1, 1, 
          hour=self.train.stations[self.dep_stn.name].hour, 
          minute=self.train.stations[self.dep_stn.name].minute
    ) 
    arrv_time = datetime(1, 1, 1, hour=self.arrival_time.hour,
                               minute=self.arrival_time.minute)
    return arrv_time - leave_time


  def time_waiting_for_train_to_str(self):
    time_waiting = self.time_waiting_for_train()
    print_str = "Wait for: {hours} {hours_str} {mins} {mins_str}"
    return self.deltas_to_str(time_waiting, print_str)

  
  def time_on_train_to_str(self):
    time_waiting = self.time_on_train()
    print_str = "Ride train for: {hours} {hours_str} {mins} {mins_str}"
    return self.deltas_to_str(time_waiting, print_str)
  

  def deltas_to_str(self, time_waiting, print_str):
    hours = time_waiting.seconds // 3600
    mins = (time_waiting.seconds // 60) % 60
    hours_str = "hour" if hours == 1 else "hours"
    mins_str = "min" if mins == 1 else "mins" 
    return print_str.format(hours=hours, hours_str=hours_str,
                            mins=mins, mins_str=mins_str)


  def __str__(self):
    dep_stn_arrival_time = self.dep_stn_arrival_time()
    s =  cleandoc(f"""
      Current time: {self.dep_time.time()}
      Time to {self.dep_stn.name} stn: {self.time_to_stn}
      Arrive at {self.dep_stn.name} at: {dep_stn_arrival_time}
      {self.time_waiting_for_train_to_str()}
      Depart train {self.train.number} {self.train.bound_to_str()} at: {self.train.stations[self.dep_stn.name]}
      {self.time_on_train_to_str()}
      Arrive at {self.dest_stn.name} stn at: {self.arrival_time}
      """)
    return s


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
    dep_time = drop_mins_secs(dep_time)
    ttstns_stns = self.ttstns_stns_to_closest_stns(
      origin, num_stations, *args, **kwargs)
    arrivals_res = []
    for ttstn, stn in ttstns_stns:
      stn_dep_time = dep_time + ttstn 
      for arrv_time, train in self.cnavi.earliest_arrival_times(
        stn_dep_time, stn, dest_sta, max_trains 
      ):
        cn_res = CalTrainNaviRes(
          arrival_time=arrv_time,
          time_to_stn=ttstn,
          dep_stn=stn,
          train=train,
          dep_time=dep_time,
          dest_stn=dest_sta
        )
        arrivals_res.append(cn_res)
    return sorted(arrivals_res, key=lambda k: k.arrival_time)

  
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