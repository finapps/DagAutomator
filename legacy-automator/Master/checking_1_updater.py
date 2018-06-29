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
tree = ET.parse('xml_files/master_checking_1.xml')
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
		youngest_date = max(newArray)
		todayDate = datetime.now()
		dateDiff = abs((todayDate - youngest_date).days)
		newDate = date + dateutil.relativedelta.relativedelta(days=dateDiff)
		date = str(newDate.isoformat())
		newDateArray.append(date)

	return newDateArray

def updateXML(xmlFile):
	originalDatesArr = oldDate(xmlFile)
	adjustedDatesArr = newDate(originalDatesArr)
	transDates = xmlFile.findall('.//transDate')
	for num in range(0, len(transDates)):
		transDates[num].text = adjustedDatesArr[num]


	#Write back to a file
	print("Checking 1 ==> XML Generated")


	now = datetime.now()
	actual_time = str(now.strftime("%Y-%m-%d"))
	save_path = r'generated_dag_files'
	complete_name = os.path.join(save_path, str(actual_time) + "_checking_01.xml")
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
