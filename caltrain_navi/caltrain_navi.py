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

class Bound(Enum):
  NB = auto()
  SB = auto()
  
class Day(Enum):
  WEEKDAY = auto()
  WEEKEND = auto()

@dataclass
class Train:
  number: int = 0
  service_type: Optional[ServiceType] = None 
  stations: Dict[str, time] = field(default_factory=dict) 
  Bound: Bound = Bound.NB
  weekday: bool = True

@dataclass
class Station:
  name: str
  zone: int
  times_trains: List[Tuple[time, Train]]

  def earliest_arrival_times(self, 
                             time: time, 
                             dest: 'Station', 
                             stations_to_trains: Dict[str, Train],
                             day: Day = Day.WEEKDAY,
                             bound: Bound = Bound.NB,
                             max_trains: int = 3) -> List[time]:
    relevant_trains = self.relevant_trains(dest, stations_to_trains, day, bound)
    trains_to_dest = self.relevant_time_trains(relevant_trains)
    trains = self.earliest_trains(time, trains=trains_to_dest, 
                                  max_trains=max_trains) 
    return self.arrival_times(trains, dest)
    
  def arrival_times(self, trains: List['Train'], dest: 'Station', 
                        sort: bool = True) -> List[time]:
    return sorted((train.stations[dest.name] for train in trains))

  def relevant_time_trains(self, trains: List[Train] )-> List[Tuple[time, Train]]:
    return list(filter(lambda times_train: \
      times_train[1].number in trains, self.times_trains))
  
  def relevant_trains(self, dest: 'Station',
                      stations_to_trains: Dict[str, Train],
                      day: Day = Day.WEEKDAY,
                      bound: Bound = Bound.NB) -> List[Train]:
    return stations_to_trains[dest.name][day.name][bound.name]

  def earliest_trains(self, time: time, 
                      trains: List[Train] = None, 
                      max_trains: int = 3) -> List[Train]:
    trains = self.times_trains if trains is None else trains
    if not self.trains_are_sorted(trains=trains):
      raise Exception("Times trains tuples are not in sorted order")
    idx = bisect_left(trains, (time, None))
    return list(list(zip(*trains))[1])[idx: min(idx+max_trains, len(trains))]
    
  def trains_are_sorted(self, trains: List[Train] = None) -> bool:
    trains = self.times_trains if trains is None else trains
    return all(trains[i][0] < trains[i+1][0] for i in range(len(trains)-1))

