from time import gmtime, strftime
from datetime import datetime, timedelta, date as dt
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random
import os.path

# Global Variables
global updatedDate
global dateDiff

# Open File to be modified
tree = ET.parse('fnma_checking_case3.xml')
datesArray = []



# Parser to convert date from ISOFormat to Date Object
# This allows us to manipulate the date range.
def getDateTimeFromISO8601String(i):
  d = dateutil.parser.parse(i)
  return d



def oldDate(xmlFile):
	transactions = tree.iter('transaction')
	for transaction in transactions:
		transDate = transaction.find('transDate').text
		#print(transDate)
		transactionDate = getDateTimeFromISO8601String(transDate)
		#print(transactionDate)
		datesArray.append(transactionDate)
		#print(datesArray)
		newArray = datesArray
		#print(newArray)
		#dateArray = list(newArray)
	#print(dateArray)
	return newArray

def newDate(newArray):
	newDateArray = []
	for date in newArray:
		#print(date)
		youngest_date = max(newArray)
		#print(youngest_date)
		todayDate = datetime.now()
		dateDiff = abs((todayDate - youngest_date).days)
		#print(dateDiff)
		newDate = date + dateutil.relativedelta.relativedelta(days=dateDiff)
		#print(newDate)
		date = str(newDate.isoformat())
		newDateArray.append(date)
		#print(newDateArray)
	return newDateArray

def updateXML(xmlFile):
	#print(newDateArray)
	#print(tree.findall('.//transDate')[0].text)
	# for dateObj in tree.findall('.//transDate'): # for date in XMLtransDates
	#	  print(dateObj.text)
	#	  dateObj.text = newDateArray[dateObj]
	#	  print(dateObj)
	#	  break
	#print(xmlFile)
	originalDatesArr = oldDate(xmlFile)
	#print(originalDatesArr)
	adjustedDatesArr = newDate(originalDatesArr)
	#print(adjustedDatesArr)
	#transactions = xmlFile.iter('transDate')
	#for transaction in transactions:
	transDates = xmlFile.findall('.//transDate')
	for num in range(0, len(transDates)):
		#print(transDates[0])
		#transDate = transaction.find('transDate')
		#print("Original Value " + str(transDates[num].text))
		#print("New Value " + str(adjustedDatesArr[num]))
		transDates[num].text = adjustedDatesArr[num]
		#print("Final Value " + str(transDates[num].text))


	#Write back to a file
	print("XML Generated")

	now = datetime.now()
	actual_time = str(now.strftime("%Y-%m-%d"))
	save_path = r'generated_RI_files'
	abs_path = r'C:\Users\FinApps\Google Drive\DAG ACCOUNTS VALID DATA\RiskInsight'
	complete_name = os.path.join(save_path, str(actual_time) + "_fnma_checking_case3.xml")
	abs_complete_name = os.path.join(abs_path, str(actual_time) + "_fnma_checking_case3.xml")
	xmlFile.write(complete_name, xml_declaration=True)
	xmlFile.write(abs_complete_name, xml_declaration=True)

	return None

def testModule(dayDiff, youngest, today):
	print ("\nToday's Date: " + str(today) + "\n")
	print ("Most Recent Transaction Date: " + str(youngest) + "\n")
	print ("Day Difference: " + str(dayDiff) + "\n")
	return (dayDiff, youngest, today)

#Update XMLFile
updateXML(tree)
