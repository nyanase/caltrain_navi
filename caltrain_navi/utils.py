import re
from datetime import datetime, time, timedelta
import json

def duration_to_time(duration):
  regex = r'((?P<hour>\d+) hours? )?(?P<minute>\d+) mins?'
  m = re.match(regex, duration)
  return match_to_time(m)


def match_to_time(m):
  hour, minute = m.group('hour'), m.group('minute')
  hour = to_int_or_zero(hour)
  minute = to_int_or_zero(minute)
  return timedelta(hours=hour, minutes=minute)


def to_int_or_zero(str):
  return 0 if str is None else int(str) 


def duration_from_element(element):
  return element["duration"]["text"] 


def get_coords_from_str(str):
  regex = r'\(?(?P<lat>[\d\-\.]+), (?P<lng>[\d\-\.]+)\)?'
  m = re.match(regex, str)
  if not m: return None
  return float(m.group('lat')), float(m.group('lng'))


def format_coords(str):
    coords = str.replace(',', '').split()
    return float(coords[0]), float(coords[1])
  

def dict_vals_to_time(dict_):
  for key, val in dict_.items():
    dict_[key] = datetime.strptime(val, "%I:%M%p").time() 
  return dict_


def load_data(path):
  fp = open(path, 'r')
  data = json.loads(fp.read())
  fp.close()
  return data


def drop_mins_secs(dt):
  return dt.replace(second=0, microsecond=0)