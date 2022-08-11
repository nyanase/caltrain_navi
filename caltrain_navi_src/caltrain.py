from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from types import ClassMethodDescriptorType
from typing import Dict, List, Tuple, Optional
from datetime import time
from bisect import bisect_left
import json
from datetime import datetime

class Bound(Enum):
  NB = auto()
  SB = auto()
  
class Day(Enum):
  WEEKDAY = auto()
  WEEKEND = auto()

@dataclass
class Train:
  class ServiceType(Enum):
    L1 = auto()
    L2 = auto()
    L3 = auto()
    L4 = auto()
    L5 = auto()
    B7 = auto()

  number: int = 0
  service_type: Optional[ServiceType] = None 
  stations: Dict[str, time] = field(default_factory=dict) 
  bound: Bound = Bound.NB
  day: Day = Day.WEEKDAY

@dataclass
class Station:
  name: str
  zone: int
  order: int #from South to North 
  times_trains: List[Tuple[time, Train]] = field(default_factory=list)
  
  def __str__(self) -> str:
    times_trains_str = "["
    for time_train in self.times_trains:
      times_trains_str += f"({time_train[0]}, Train(number='{time_train[1].number}'), " 
    times_trains_str += "]"
    return f"Station(name='{self.name}, zone='{self.zone}', times_trains={times_trains_str})"

class CaltrainNavi:
  
  def __init__(self) -> None:
    self.trains: Dict[str, Train] = {}
    self.stations: Dict[str, Station] = {} 
    self.stations_to_trains:Dict[str, str, str, List[Train]] = \
      defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    self.day = Day.WEEKDAY

  def load_trains_and_stations(self, trains_path, stations_path, 
                               update_station_train=True):
    self.load_trains_data(trains_path)
    self.load_stations_data(stations_path)
    if update_station_train: self.update_stations_to_trains()
    
  def earliest_arrival_times(self, 
                            dep_time: datetime, 
                            dep_sta: Station,
                            dest_sta: Station,
                            max_trains: int = 3) -> List[time]:
    relevant_trains = self.relevant_trains(dep_sta, dest_sta, dep_time)
    trains_to_dest_sta = self.relevant_time_trains(dep_sta, relevant_trains)
    trains = self.earliest_trains(dep_time, time_trains=trains_to_dest_sta, 
                                  max_trains=max_trains) 
    return self.arrival_times(trains, dest_sta)
  
  def arrival_times(self, trains: List['Train'], dest_sta: 'Station', 
                        sort: bool = True) -> List[time]:
    return sorted((train.stations[dest_sta.name] for train in trains))

  def relevant_time_trains(self, dep_sta: Train, trains: List[Train] )-> List[Tuple[time, Train]]:
    return list(filter(lambda times_train: \
      times_train[1] in trains, dep_sta.times_trains))
  
  def relevant_trains(self, dep_sta: Station, 
                      dest_sta: Station,
                      dep_time: datetime) -> List[Train]:
    day = Day.WEEKDAY if dep_time.weekday() < 5 else Day.WEEKEND
    bound = Bound.NB if dep_sta.order < dest_sta.order else Bound.SB
    try:
      trains = self.stations_to_trains[dest_sta.name][day.name][bound.name]
    except:
      raise KeyError(f"The mapping from station to train for {dest_sta.name}, {day}, {bound}")
    return trains

  def earliest_trains(self, dep_time: datetime, 
                      time_trains: List[Tuple[time, Train]], 
                      max_trains: int = 3) -> List[Train]:
      
    if not self.trains_are_sorted(time_trains):
      #TODO: sort trains
      raise Exception("Times trains tuples are not in sorted order")
    idx = bisect_left(time_trains, (dep_time.time(), None))
    return list(list(zip(*time_trains))[1])[idx: min(idx+max_trains, len(time_trains))]
    
  @staticmethod
  def trains_are_sorted(time_trains: List[Train] = None) -> bool:
    return all(time_trains[i][0] < time_trains[i+1][0] for i in range(len(time_trains)-1))
    
  def load_trains_data(self, path):
    trains_dicts = self.load_data(path)
    for train_dict in trains_dicts:
      train = self.build_train_from_dict(train_dict)
      self.trains[train.number] = train
    return True
  
  def load_stations_data(self, path):
    stations_dicts = self.load_data(path)
    for station_dict in stations_dicts:
      station = Station(
        name=station_dict["name"],
        zone=station_dict["zone"],
        order=station_dict["order"],
        times_trains=self.update_times_trains(station_dict["times_trains"]) 
      )
      self.stations[station.name] = station
    return True 

  def build_train_from_dict(self, train_dict):
    return Train(
      number=train_dict["number"],
      service_type=Train.ServiceType[f"{train_dict['service_type']}"],
      bound=Bound[f"{train_dict['bound']}"],
      day=Day[f"{train_dict['day']}"],
      stations=self.dict_vals_to_time(train_dict["stations"]) 
    )

  def update_times_trains(self, old_tts, sort=True):
    times_trains = []
    for old_tt in old_tts:
      tt_time, tt_number = old_tt[0], old_tt[1]
      try:
        times_trains.append(
          (datetime.strptime(tt_time, "%I:%M%p").time(), 
          self.trains[tt_number])
        )
      except KeyError:
        raise KeyError(f"The train with number {tt_number} was not found in train_lkup dict")
    if sort: 
      return sorted(times_trains, key=lambda times_train: times_train[0])
    return times_trains
      

  def update_stations_to_trains(self):
    for _, station in self.stations.items():
      for _, train in station.times_trains:
        self.stations_to_trains[f"{station.name}"][f"{train.day.name}"][f"{train.bound.name}"].append(train)

  @staticmethod
  def dict_vals_to_time(dict_):
    for key, val in dict_.items():
      dict_[key] = datetime.strptime(val, "%I:%M%p").time() 
    return dict_
  
  @staticmethod
  def load_data(path):
    fp = open(path, 'r')
    data = json.loads(fp.read())
    fp.close()
    return data
  