import dateutil.parser
from datetime import datetime, timedelta

now = datetime.now()
print now

date = now.isoformat()
print date

def getDateTimeFromISO8601String(i):
	d = dateutil.parser.parse(i)
	return d

newDate = getDateTimeFromISO8601String(date)	

#newDate = now - timedelta(days=-90)
print newDate

changedDate = newDate - timedelta(days=90)
print changedDate
print changedDate.isoformat()



#date = (parser.parse(now))
#print(date.isoformat())


