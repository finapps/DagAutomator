from time import gmtime, strftime
from datetime import datetime, timedelta, date as dt
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random
import os.path
import boto3

# Global Variables
global updatedDate
global dateDiff

# Open File to be modified
tree = ET.parse('../xml_files/2_trans.xml')
datesArray = []
s3 = boto3.client('s3')

# Parser to convert date from ISOFormat to Date Object
# This allows us to manipulate the date range.
def getDateTimeFromISO8601String(i):
  d = dateutil.parser.parse(i)
  return d

def oldDate(xmlFile):
	transactions = tree.iter('transaction')
	for transaction in transactions:
		transDate = transaction.find('transDate').text
		transactionDate = getDateTimeFromISO8601String(transDate)
		datesArray.append(transactionDate)
		newArray = datesArray
	return newArray

def newDate(newArray):
	newDateArray = []
	for date in newArray:
		#print(date)
		youngest_date = max(newArray)
		#print(youngest_date)
		yesterdayDate = datetime.now() - timedelta(1)
		#todayDate = datetime.now()
		dateDiff = abs((yesterdayDate - youngest_date).days)
		#print(dateDiff)
		newDate = date + dateutil.relativedelta.relativedelta(days=dateDiff)
		#print(newDate)
		date = str(newDate.isoformat())
		newDateArray.append(date)
		#print(newDateArray)
	return newDateArray

def updateXML(xmlFile):
	originalDatesArr = oldDate(xmlFile)
	adjustedDatesArr = newDate(originalDatesArr)
	transDates = xmlFile.findall('.//transDate')
	for num in range(0, len(transDates)):
		transDates[num].text = adjustedDatesArr[num]

	#Write back to a file
	print("2_Transaction XML ==> Complete")

	now = datetime.now()
	actual_time = str(now.strftime("%Y-%m-%d"))
	save_path = r'../edge_cases'
	complete_name = os.path.join(save_path, str(actual_time) + "_2_trans.xml")
	xmlFile.write(complete_name, xml_declaration=True)
	filename = complete_name
	bucket_name = 'dagautomator'
	s3.upload_file(filename, bucket_name, filename)
	return None

def testModule(dayDiff, youngest, today):
	print ("\nToday's Date: " + str(today) + "\n")
	print ("Most Recent Transaction Date: " + str(youngest) + "\n")
	print ("Day Difference: " + str(dayDiff) + "\n")
	return (dayDiff, youngest, today)

#Update XMLFile
updateXML(tree)
