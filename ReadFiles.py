import datetime

time_str = str(datetime.datetime.now())
datetime.datetime.strptime(time_str, "%Y-%M")