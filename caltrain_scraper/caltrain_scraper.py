from bs4 import BeautifulSoup
import requests

START_COL = 2

def scrape_sched(sched, bound, weekday=True, stations=None):
  rows = sched.find_all("tr")
  trains = setup_trains(rows[:2], bound, weekday)
  stations = scrape_rows(rows[2:], trains, bound=bound, stations=stations)
  print(stations[-1])
  
  return trains, stations

def setup_trains(rows, bound, weekday=True):
  trains = []
  train_nums_row, train_type_row = rows[0], rows[1]
  for col in train_nums_row.find_all("td")[START_COL:]:
    trains.append({
      "name": col.get_text(), 
      "direction": bound, 
      "stations": {},
      "weekday": weekday
    })
  for i, col in enumerate(train_type_row.find_all("td")[START_COL:]):
    trains[i]["service_type"] = col.get_text() 
  return trains

def scrape_rows(rows, trains, bound="nb", stations=None):
  stations_ = [] if stations is None else stations
  rows = rows[::-1] if bound == "SB" else rows
  i = 0
  for row in rows:
    if "zone-change" in row["class"]:
      continue
    cols = row.find_all("td")
    station = setup_station(cols) if stations is None else stations_[i]
    scrape_times(station, trains, cols, bound)
    if stations is None: stations_.append(station)
    i += 1
  return stations_

def scrape_times(station, trains, cols, bound="NB"):
  tt_bound = "times_trains_nb" if bound == "NB" else "times_trains_sb"
  for i, col in enumerate(cols[2:]):
    time = col.get_text()
    if time == "--":
      continue
    station[f"{tt_bound}"].append((time, trains[i]["name"]))
    trains[i]["stations"][f"{station['name']}"] = time
  return

def setup_station(cols):
  station = {}
  station["zone"] = cols[0].get_text()
  station["name"] = cols[1].get_text()
  station["times_trains_nb"] = [] 
  station["times_trains_sb"] = [] 
  return station

def main():
  caltrain_url = \
  "https://www.caltrain.com/schedules/pdf-schedules?active_tab=route_explorer_tab"
  caltrain_page = requests.get(caltrain_url)
  soup = BeautifulSoup(caltrain_page.content, "html.parser")
  nb_sched, sb_sched = tuple(soup.find_all("table", class_="caltrain_schedule"))
  nb_wkday_trains, stations = scrape_sched(nb_sched, bound="NB")
  sb_wkday_trains, stations = scrape_sched(sb_sched, bound="SB", stations=stations)


if __name__ == "__main__":
  main()