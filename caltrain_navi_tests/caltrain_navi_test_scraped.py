import pytest
from caltrain_navi.caltrain import CaltrainNavi, Train, Station
from datetime import datetime, time
from typing import Dict, List

trains_path = "/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json"
stations_path = "/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json" 
cn = CaltrainNavi(trains_path=trains_path, stations_path=stations_path)

def test_load_trains_and_stations():
  cn.load_trains_and_stations()
  
  assert len(cn.stations) == 30
  assert len(cn.stations_to_trains["San Mateo"]["WEEKDAY"]["NB"]) == 39

def test_earliest_arrival_times_nb():
  times = cn.earliest_arrival_times(datetime(2022, 8, 10, 6, 0), 
                                    dep_sta=cn.stations["Mountain View"], 
                                    dest_sta=cn.stations["Palo Alto"])
  assert times == [
    (time(6,10), cn.trains["401"]), 
    (time(6,21), cn.trains["701"]),
    (time(6,31), cn.trains["105"])
  ] 
  
  times = cn.earliest_arrival_times(datetime(2022, 8, 10, 17, 30), 
                                    dep_sta=cn.stations["Santa Clara"],
                                    dest_sta=cn.stations["San Francisco"])
  assert times == [
    (time(19, 0), cn.trains["413"]),
    (time(19,34), cn.trains["129"]),
    (time(20,0), cn.trains["415"])
  ]

def test_earliest_arrival_times_sb():
  times = cn.earliest_arrival_times(datetime(2022, 8, 10, 18, 0),
                                    dep_sta=cn.stations["San Francisco"],
                                    dest_sta=cn.stations["Mountain View"])
  assert times == [
    (time(18, 57), cn.trains["712"]),
    (time(19, 9), cn.trains["414"]),
    (time(19, 29), cn.trains["314"])
  ]

  times = cn.earliest_arrival_times(datetime(2022, 8, 10, 14, 45),
                                    dep_sta=cn.stations["Millbrae"],
                                    dest_sta=cn.stations["San Jose Diridon"])
  assert times == [
    (time(16,19), cn.trains["122"]),
    (time(16,30), cn.trains["408"]),
    (time(16,49), cn.trains["308"])
  ]

def test_earliest_arrival_times_weekend():
  times = cn.earliest_arrival_times(datetime(2022, 8, 13, 10, 2),
                                    dep_sta=cn.stations["Mountain View"],
                                    dest_sta=cn.stations["San Francisco"])
  assert times == [
    (time(11, 53), cn.trains["229"]),
    (time(12, 53), cn.trains["233"]),
    (time(13, 52), cn.trains["237"])
  ]

def test_max_times():
  times = cn.earliest_arrival_times(datetime(2022, 8, 10, 6, 0), 
                                    dep_sta=cn.stations["Mountain View"], 
                                    dest_sta=cn.stations["Palo Alto"],
                                    max_trains=2)
  assert times == [
    (time(6,10), cn.trains["401"]), 
    (time(6,21), cn.trains["701"])
  ]  

def test_no_times_available():
  times = cn.earliest_arrival_times(datetime(2022, 8, 10, 21, 0),
                                    dep_sta=cn.stations["Gilroy"],
                                    dest_sta=cn.stations["San Francisco"])
  assert times == []

 
