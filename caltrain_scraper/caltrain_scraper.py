from asyncore import write
from bs4 import BeautifulSoup
import requests
import json
from caltrain_addresses import station_addresses

NAME_ROW = 0
SERVICE_TYPE_ROW = 1
START_COL = 2
SETUP_ROWS = 2
CALTRAIN_URL = \
  "https://www.caltrain.com/schedules/pdf-schedules?active_tab=route_explorer_tab"


def ct_soup():
  caltrain_page = requests.get(CALTRAIN_URL)
  return BeautifulSoup(caltrain_page.content, "html.parser")


def scrape_sched(sched, bound, stations=None, prev_trains=None):
  rows = sched.find_all("tr")
  trains = setup_trains(rows[:SETUP_ROWS], bound)
  stations = scrape_rows(rows[SETUP_ROWS:], trains, bound=bound, stations=stations)
  if prev_trains: trains = prev_trains + trains
  return trains, stations


def setup_trains(rows, bound):
  trains = [] 
  train_nums_row, train_type_row = rows[NAME_ROW], rows[SERVICE_TYPE_ROW]
  for col in train_nums_row.find_all("td")[START_COL:]:
    trains.append({
      "number": col.get_text(), 
      "bound": bound, 
      "stations": {},
      "day": is_weekday_train(col) 
    })
  for i, col in enumerate(train_type_row.find_all("td")[START_COL:]):
    trains[i]["service_type"] = col.get_text() 
  return trains

def is_weekday_train(col):
  return "WEEKDAY" if col["data-service-type"] == "weekday" else "WEEKEND"

def scrape_rows(rows, trains, bound="NB", stations=None):
  stations_ = [] if stations is None else stations
  rows = rows[::-1] if bound == "SB" else rows
  i = 0
  for row in rows:
    if "zone-change" in row["class"]:
      continue
    cols = row.find_all("td")
    station = setup_station(cols, order=i) if stations is None else stations_[i]
    scrape_times(station, trains, cols)
    if stations is None: stations_.append(station)
    i += 1
  return stations_


def scrape_times(station, trains, cols):
  for i, col in enumerate(cols[2:]):
    time = col.get_text()
    if time == "--":
      continue
    station[f"times_trains"].append((time, trains[i]["number"]))
    trains[i]["stations"][f"{station['name']}"] = time
  return


def setup_station(cols, order):
  zone = cols[0].get_text()
  name = cols[1].get_text()
  station = {}
  station["zone"] = zone
  station["name"] = name
  station["order"] = order
  station["times_trains"] = [] 
  station["address"] = station_addresses[name][0] 
  station["coordinates"] = station_addresses[name][1] 
  return station


def write_to_file(filename, data):
  with open(filename, 'w') as fp:
    json.dump(data, fp)
  return


def main():
  wkday_soup = ct_soup() 
  nb_wkday_sched, sb_wkday_sched = tuple(wkday_soup.find_all("table",
                                          class_="caltrain_schedule"))
  trains, stations = scrape_sched(nb_wkday_sched, bound="NB")
  trains, stations = scrape_sched(sb_wkday_sched, bound="SB", 
                                  stations=stations, prev_trains=trains)
  write_to_file("./scraped_data/trains.json", trains)
  write_to_file("./scraped_data/stations.json", stations)

if __name__ == "__main__":
  main()