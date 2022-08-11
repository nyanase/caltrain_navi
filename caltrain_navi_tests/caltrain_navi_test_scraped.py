import pytest
from caltrain_navi_src.caltrain import CaltrainNavi, Train, Station
from caltrain_navi_src.caltrain_data_loader import load_stations_data, load_trains_data
from datetime import time
from typing import Dict, List

cn = CaltrainNavi()
trains_path = "/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json"
stations_path = "/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json" 

def test_load_trains_and_stations():
  cn.load_trains_and_stations(trains_path=trains_path, 
                            stations_path=stations_path)
  
  # TODO: more robust tests
  assert len(cn.stations) == 30
  assert len(cn.stations_to_trains["San Mateo"]["WEEKDAY"]["NB"]) == 39

def test_earliest_arrival_times_nb():
  times = cn.earliest_arrival_times(time(6,0), 
                                    cn.stations["Mountain View"], 
                                    cn.stations["Palo Alto"])
  assert times == [time(6,10), time(6,21), time(6,31)] 
  
  times = cn.earliest_arrival_times(time(17, 30), 
                                    cn.stations["Santa Clara"],
                                    cn.stations["San Francisco"])
  assert times == [time(19, 0), time(19,34), time(20,0)]

def test_earliest_arrival_times_sb():
  times = cn.earliest_arrival_times(time(18, 0),
                                    cn.stations["San Francisco"],
                                    cn.stations["Mountain View"])
  assert times == [time(18, 57), time(19, 9), time(19, 29)]

  times = cn.earliest_arrival_times(time(14, 45),
                                    cn.stations["Millbrae"],
                                    cn.stations["San Jose Diridon"])
  assert times == [time(16,19), time(16,30), time(16,49)]

 
