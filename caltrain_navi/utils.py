import re
from datetime import time

def duration_to_time(duration):
  regex = r'((?P<hour>\d+) hours? )?(?P<minute>\d+) mins?'
  m = re.match(regex, duration)
  return match_to_time(m)


def match_to_time(m):
  hour, minute = m.group('hour'), m.group('minute')
  hour = to_int_or_zero(hour)
  minute = to_int_or_zero(minute)
  return time(hour=hour, minute=minute)


def to_int_or_zero(str):
  return 0 if str is None else int(str) 


def duration_from_element(element):
  return element["duration"]["text"] 


def get_coords_from_str(str):
  regex = r'\(?(?P<lat>[\d\-\.]+), (?P<lng>[\d\-\.]+)\)?'
  m = re.match(regex, str)
  if not m: return None
  return float(m.group('lat')), float(m.group('lng'))

