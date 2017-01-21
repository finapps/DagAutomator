from time import gmtime, strftime
from datetime import datetime, timedelta
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random


now = datetime.now()
print(now)

beginDate = now + dateutil.relativedelta.relativedelta(months=-3)
print(beginDate)

#date = now.isoformat()
#print date

#def getDateTimeFromISO8601String(i):
#	d = dateutil.parser.parse(i)
#	return d

#newDate = getDateTimeFromISO8601String(date)	

#newDate = now - timedelta(days=-90)
#print newDate

#changedDate = newDate - timedelta(days=90)
#print changedDate
#print changedDate.isoformat()





#date = (parser.parse(now))
#print(date.isoformat())


