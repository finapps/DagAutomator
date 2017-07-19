from time import gmtime, strftime
from datetime import datetime, timedelta, date as dt
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random
import os.path
from config import INFOLDER
from config import OUTFOLDER

# Global Variables
global updatedDate
global dateDiff


datesArray = []

# Parser to convert date from ISOFormat to Date Object
# This allows us to manipulate the date range.
def getDateTimeFromISO8601String(i):
  d = dateutil.parser.parse(i)
  return d


def oldDate(xmlFile):
    transactions = xmlFile.iter('transaction')
    for transaction in transactions:
        transDate = transaction.find('transDate')
        if transDate == None:
            transDate = transaction.find('date').text
        else:
            transDate = transDate.text
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

def updateXML(xmlFile, filename):
    originalDatesArr = oldDate(xmlFile)
    adjustedDatesArr = newDate(originalDatesArr)
    transDates = xmlFile.findall('.//transDate')
    if transDates == []:
        transDates = xmlFile.findall('.//date')
    for num in range(0, len(transDates)):
        transDates[num].text = adjustedDatesArr[num]

    print("XML Generated")

    now = datetime.now()
    actual_time = str(now.strftime("%Y-%m-%d"))

    xmlFile.write(OUTFOLDER + "/" + filename, xml_declaration=True)

    return None

def testModule(dayDiff, youngest, today):
	print ("\nToday's Date: " + str(today) + "\n")
	print ("Most Recent Transaction Date: " + str(youngest) + "\n")
	print ("Day Difference: " + str(dayDiff) + "\n")
	return (dayDiff, youngest, today)

def main():
    for filename in os.listdir(OUTFOLDER):
        os.remove(OUTFOLDER + "/" + filename)
    for filename in os.listdir(INFOLDER):
        tree = ET.parse(INFOLDER + "/" + filename)
        datesArray = []
        updateXML(tree,filename)

main()
