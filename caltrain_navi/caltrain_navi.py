from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Tuple, Optional
from datetime import time
from bisect import bisect_left
class ServiceType(Enum):
  L1 = auto()
  L2 = auto() 
  L4 = auto()
  B7 = auto()

class Direction(Enum):
  NB = auto()
  SB = auto()

stations_to_services: Dict['Station', List['ServiceType']] = {
  "Mountain View": [ServiceType.L4, ServiceType.L1, ServiceType.B7],
  "Palo Alto": [ServiceType.L4, ServiceType.L1, ServiceType.B7] 
}

@dataclass
class Train:
  number: int
  service_type: Optional[ServiceType] = None 
  stations: Dict[str, time] = field(default_factory=dict) 
  direction: Direction = Direction.NB

@dataclass
class Station:
  name: str
  zone: int
  times_trains: List[Tuple[time, Train]]

  def earliest_arrival_times(self, time: time, 
                      dest: 'Station', 
                      max_trains: int = 3):
    trains_to_dest = self.relevant_train_lines(dest)
    trains = self.earliest_trains(time, trains=trains_to_dest, 
                                  max_trains=max_trains) 
    return self.arrival_times(trains, dest)
    
  def arrival_times(self, trains: List['Train'], dest: 'Station', 
                        sort: bool = True):
    return sorted((train.stations[dest.name] for train in trains))

  def relevant_train_lines(self, dest: 'Station'):
    services = stations_to_services[dest.name]
    return list(filter(lambda times_train: times_train[1].service_type in services, 
                            self.times_trains))

  def earliest_trains(self, time: time, 
                      trains: List[Train] = None, max_trains: int = 3):
    trains = self.times_trains if trains is None else trains
    if not self.trains_are_sorted(trains=trains):
      raise Exception("Times trains tuples are not in sorted order")
    idx = bisect_left(trains, (time, None))
    return list(list(zip(*trains))[1])[idx: min(idx+max_trains, len(trains))]
    
  def trains_are_sorted(self, trains: List[Train] = None):
    trains = self.times_trains if trains is None else trains
    return all(trains[i][0] < trains[i+1][0] for i in range(len(trains)-1))

