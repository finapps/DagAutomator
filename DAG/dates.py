<<<<<<< HEAD
import datetime
import dateutil


now = datetime.datetime.now()

print now

#def getDateTimeFromISO8601String(s):
#    d = dateutil.parser.parse(s)
#    return d
=======
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


>>>>>>> 3c0a9d1f31fde243bf0aae25a9851a1ac50553c9
