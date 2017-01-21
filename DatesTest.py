from time import gmtime, strftime
from datetime import datetime, timedelta as dt
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random



# Open File to be modified
tree = ET.parse('user.xml')
root = tree

# Parser to convert date from ISOFormat to Date Object
# This allows us to manipulate the date range.
def getDateTimeFromISO8601String(i):
	d = dateutil.parser.parse(i)
	return d

newDate = getDateTimeFromISO8601String(date) 
# Checks date and updates if outside 90 day range

for dates in root.iter('transDate'):
  now = datetime.now() # This is Date Object
  datesArray = []
  originalDate = datesArray.append(newDate)
  print(dates.text)


