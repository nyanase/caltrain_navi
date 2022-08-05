import pytest
from caltrain_navi.caltrain_navi import Train, Station, ServiceType
from datetime import time

mountain_view = Station("Mountain View", 3, None)
palo_alto = Station("Palo Alto", 3, None)
t_401 = Train(401, ServiceType.L4)
t_105 = Train(105, ServiceType.L1)
t_701 = Train(701, ServiceType.B7)

mountain_view.times_trains = [
  (time(6, 3), t_401),
  (time(6, 13), t_701),
  (time(6, 19), t_105),
] 
palo_alto.times_trains = [
  (time(6, 10), t_401),
  (time(6, 21), t_701),
  (time(6, 31), t_105),
]

t_401.stations = {
  f'{mountain_view.name}': time(6, 3),
  f'{palo_alto.name}': time(6, 10)
}
t_105.stations = {
  f'{mountain_view.name}': time(6, 19),
  f'{palo_alto.name}': time(6, 31)
}
t_701.stations = {
  f'{mountain_view.name}': time(6, 13),
  f'{palo_alto.name}': time(6, 21)
}

def test_trains_are_sorted():
  assert mountain_view.trains_are_sorted() == True

def test_earliest_trains_for_time():
  assert mountain_view.earliest_trains(
    time(6, 4), max_trains=2) == [t_701, t_105] 

def test_earliest_arrival_times():
  assert mountain_view.earliest_arrival_times(time(6,0), palo_alto) \
    == [time(6,10), time(6,21), time(6,31)]
    
