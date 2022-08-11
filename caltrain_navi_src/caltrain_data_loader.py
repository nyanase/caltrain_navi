from typing import List
from .caltrain import Train, Station, Bound, Day
import json
from datetime import datetime

def load_data(path):
  fp = open(path, 'r')
  data = json.loads(fp.read())
  fp.close()
  return data

def load_stations_data(path, trains_dict) -> List[Station]:
  stations_dicts = load_data(path)
  stations = []
  for station_dict in stations_dicts:
    station = Station(
      name=station_dict["name"],
      zone=station_dict["zone"],
      times_trains=update_times_trains(station_dict["times_trains"], 
                                       trains_dict) 
    )
    stations.append(station)
  return stations

def update_times_trains(old_tts, trains_dict):
  times_trains = []
  for old_tt in old_tts:
    tt_time, tt_number = old_tt[0], old_tt[1]
    times_trains.append(
      (datetime.strptime(tt_time, "%H:%M%p").time(), trains_dict[tt_number])
    )
  return times_trains

def trains_list_to_dict(trains):
  trains_dict = {}
  for train in trains:
    trains_dict[train.number] = train
  return trains_dict
  
def load_trains_data(path) -> List[Train]:
  trains_dicts = load_data(path)
  trains = []
  for train_dict in trains_dicts:
    train = Train(
      number=train_dict["number"],
      service_type=str_to_service_type(train_dict["service_type"]),
      bound=str_to_bound(train_dict["bound"]),
      weekday=str_to_day(train_dict["day"]),
      stations=dict_vals_to_time(train_dict["stations"])
    )
    trains.append(train)
  return trains

def str_to_service_type(str):
  return Train.ServiceType[f"{str}"] 

def str_to_bound(str):
  return Bound[f"{str}"]

def str_to_day(str):
  return Day[f"{str}"]
  
def dict_vals_to_time(dict_):
  for key, val in dict_.items():
    dict_[key] = datetime.strptime(val, "%H:%M%p").time() 
  return dict_

def main():
  trains = load_trains_data("/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json")
  trains_dict = trains_list_to_dict(trains)
  stations = load_stations_data("/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json", trains_dict)
  for station in stations:
    print(station.name)

if __name__ == "__main__":
  main()