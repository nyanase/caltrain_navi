# import pytest
# from caltrain_navi_src.caltrain import Train, Station
# from caltrain_navi_src.caltrain_data_loader import load_stations_data, load_trains_data
# from datetime import time
# from typing import Dict, List

# # trains = load_trains_data("../caltrain_scraper/scraped_data/trains.json")
# # trains_dict = trains_list_to_dict(trains)
# # stations = load_stations_data("../caltrain_scraper/scraped_data/stations.json", trains_dict)


# mountain_view = Station("Mountain View", 3, None)
# palo_alto = Station("Palo Alto", 3, None)
# t_401 = Train(401, Train.ServiceType.L4)
# t_105 = Train(105, Train.ServiceType.L1)
# t_701 = Train(701, Train.ServiceType.B7)

# mountain_view.times_trains = [
#   (time(6, 3), t_401),
#   (time(6, 13), t_701),
#   (time(6, 19), t_105),
# ] 
# palo_alto.times_trains = [
#   (time(6, 10), t_401),
#   (time(6, 21), t_701),
#   (time(6, 31), t_105),
# ]

# t_401.stations = {
#   f'{mountain_view.name}': time(6, 3),
#   f'{palo_alto.name}': time(6, 10)
# }
# t_105.stations = {
#   f'{mountain_view.name}': time(6, 19),
#   f'{palo_alto.name}': time(6, 31)
# }
# t_701.stations = {
#   f'{mountain_view.name}': time(6, 13),
#   f'{palo_alto.name}': time(6, 21)
# }
# stations_to_trains: Dict[str, Dict[str, Dict[str, List[Train]]]] = {
#   "Mountain View": {
#     "WEEKDAY": {
#       "NB": [t_401, t_701, t_105],
#       "SB": []
#     },
#     "WEEKEND": {
#       "NB": [],
#       "SB": []
#     }
#   },
#   "Palo Alto": {
#     "WEEKDAY": {
#       "NB": [t_401, t_701, t_105],
#       "SB": []
#     },
#     "WEEKEND": {
#       "NB": [],
#       "SB": []
#     }
#   },
# }

# def test_trains_are_sorted():
#   assert mountain_view.trains_are_sorted() == True

# def test_earliest_trains_for_time():
#   assert mountain_view.earliest_trains(
#     time(6, 4), max_trains=2) == [t_701, t_105] 

# def test_earliest_arrival_times():
#   assert mountain_view.earliest_arrival_times(time(6,0), 
#                                               palo_alto,
#                                               stations_to_trains=stations_to_trains) \
#     == [time(6,10), time(6,21), time(6,31)]
    
