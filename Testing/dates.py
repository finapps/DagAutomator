from time import gmtime, strftime
from datetime import datetime, timedelta as dt
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random



# Open File to be modified
tree = ET.parse('user.xml')
root = tree
now = datetime.now()
#print (now)



def getDateTimeFromISO8601String(i):
	d = dateutil.parser.parse(i)
	return d

for dates in root.iter('transDate'):
	todayDate = datetime.now()
	beginDate = todayDate + dateutil.relativedelta.relativedelta(months=-3)
	originalDate = dates.text
	transactionDate = getDateTimeFromISO8601String(originalDate)
	newArray = []
	newArray.extend(transactionDate)
	#newArray.append(transactionDate)	
	print (newArray)

date = now.isoformat()
#print (date)



newDate = getDateTimeFromISO8601String(date)



#newDate = now - timedelta(days=-90)
#print (newArray)

'''
changedDate = newDate - timedelta(days=90)
print (changedDate)
print (changedDate.isoformat())
'''


#date = (parser.parse(now))
#print(date.isoformat())



