from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple
from datetime import time
from bisect import bisect_left, bisect_right

services_to_stations: Dict['ServiceType', 'Station'] = {}
stations_to_services: Dict['Station', 'ServiceType'] = {}

class ServiceType(Enum):
  L1 = auto()
  L2 = auto() 
  L4 = auto()
  B7 = auto()

@dataclass
class Train:
  number: int
  service_type: ServiceType 
  stations: Dict[str, time] 

@dataclass
class Station:
  name: str
  zone: int
  trains: List[Tuple[time, Train]]

  def get_earliest_trains_for_time_and_dest(self, time: time, 
                                            dest: 'Station', 
                                            num_trains: int = 3):
    services = stations_to_services[dest]
    trains_to_dest = filter(lambda train: train.service_type in services, 
                            self.trains)
    return self.get_earliest_trains_for_time(time, trains=trains_to_dest, 
                                             num_trains=num_trains)

  def get_earliest_trains_for_time(self, time: time, 
                                   trains: List[Train] = None, 
                                   num_trains: int = 3):
    trains = self.trains if trains is None else trains
    if not self.trains_are_sorted(trains=trains):
      raise Exception("Trains are not in sorted order")
    idx = bisect_left(trains, (time, None))
    return trains[idx: min(idx+num_trains, len(trains))]
    
  def trains_are_sorted(self, trains: List[Train] = None):
    trains = self.trains if trains is None else trains
    return all(trains[i][0] < trains[i+1][0] for i in range(len(trains)-1))

