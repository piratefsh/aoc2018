import re

class LogEntry:
  def __init__(self, date, hour, minute, event="", gid=None):
    self.date = date
    self.hour = hour
    self.minute = minute
    self.ihour = int(hour)
    self.iminute = int(minute)
    self.event = event
    self.gid = gid
    self.days = int(date[2:4]) * 30 + int(date[4:])
    self._minutes = int(self.minute) + int(self.hour) * 60 + (self.days * 24 * 60)

  def __lt__(self, other):
    return self._minutes < other._minutes
  def __le__(self, other):
    return self._minutes <= other._minutes
  def __eq__(self, other):
    return self._minutes == other._minutes
  def __gt__(self, other):
    return self._minutes >= other._minutes
  def __ge__(self, other):
    return self._minutes >= other._minutes

  def __sub__(self, other):
    return self._minutes - other._minutes

  def __repr__(self):
    return "gid:{gid} date:{date} hour:{hour} minute:{minute} event:{event}".format(
      gid=self.gid, date=self.date, hour=self.hour, minute=self.minute, event=self.event)

assert (LogEntry('20180102', '00', '01') - LogEntry('20180101', '23', '59') == 2)

def parse_date(date_time):
  raw_date, raw_time = date_time.split(' ')
  date = "".join(raw_date.split('-'))
  hr, minute = raw_time.split(':')
  return date, hr, minute
  
def parse_event(event):
  if event.startswith('Guard'):
    gid, = re.match(r'Guard #(\d*).*', event).groups()
    return 'start', gid 
  elif event.startswith('wakes up'):
    return 'on', None
  elif event.startswith('falls asleep'):
    return 'off', None

  raise Error("Invalid event %s" % event)

def parse(line):
  date_time, event = re.match(r'\[(.*)\] (.*)', line).groups()
  date, hr, minute = parse_date(date_time)
  etype, gid = parse_event(event)
  return LogEntry(date, hr, minute, etype, gid)

def parse_and_sort(file):
  last_gid = None
  logs = []
  sorted_by_date = sorted([parse(line) for line in file])
  for log in sorted_by_date:
    if log.gid is not None:
      last_gid = log.gid 
    else:
      log.gid = last_gid
    logs.append(log)

  return sorted_by_date

# Strategy 1: 
# Find the guard that has the most minutes asleep. 
# What minute does that guard spend asleep the most?
def part_a(logs):
  pass

def sleepist_minute(logs, gid):
  schedule = [0] * 60
  highest = 0
  last_awake = None
  for log in logs:
    if log.gid != gid:
      continue
    if log.event == 'off':
      last_awake = log
    elif log.event == 'on':
      for m in range(last_awake.iminute, log.iminute):
        schedule[m] += 1
        if schedule[m] > schedule[highest]:
          highest = m 
  return highest

def sleepiest_guard(logs):
  guards = dict()
  highest = None
  last_awake = None
  for log in logs:
    if log.event == 'off':
      last_awake = log
    elif log.event == 'on':
      diff = log - last_awake
      guards[log.gid] = guards[log.gid] + diff if log.gid in guards else diff
      highest = log.gid if highest is None or guards[log.gid] > guards[highest] else highest
  return highest

assert(parse_date('1518-11-01 23:59') == ('15181101', '23', '59'))
assert(str(parse('[1518-05-12 00:44] falls asleep')) == 'gid:None date:15180512 hour:00 minute:44 event:off')
assert(str(parse('[1518-11-01 00:01] Guard #10 begins shift')) == 'gid:10 date:15181101 hour:00 minute:01 event:start')
assert(','.join(map(str, parse_and_sort(open('sample.txt')))) == "gid:10 date:15181101 hour:00 minute:00 event:start,gid:10 date:15181101 hour:00 minute:05 event:off,gid:10 date:15181101 hour:00 minute:25 event:on,gid:10 date:15181101 hour:00 minute:30 event:off,gid:10 date:15181101 hour:00 minute:55 event:on,gid:99 date:15181101 hour:23 minute:58 event:start,gid:99 date:15181102 hour:00 minute:40 event:off,gid:99 date:15181102 hour:00 minute:50 event:on,gid:10 date:15181103 hour:00 minute:05 event:start,gid:10 date:15181103 hour:00 minute:24 event:off,gid:10 date:15181103 hour:00 minute:29 event:on,gid:99 date:15181104 hour:00 minute:02 event:start,gid:99 date:15181104 hour:00 minute:36 event:off,gid:99 date:15181104 hour:00 minute:46 event:on,gid:99 date:15181105 hour:00 minute:03 event:start,gid:99 date:15181105 hour:00 minute:45 event:off,gid:99 date:15181105 hour:00 minute:55 event:on")

sample_logs = parse_and_sort(open('sample.txt'))
sample_g = sleepiest_guard(sample_logs)
assert(sample_g == '10')
assert(sleepist_minute(sample_logs, sample_g) == 24)

input_logs = parse_and_sort(open('input.txt'))
input_g = sleepiest_guard(input_logs)
assert(input_g == '1021')
input_m = sleepist_minute(input_logs, input_g)
assert(input_m == 30)
print('answer', int(input_g) * input_m)
print('all tests pass')
