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
tree = ET.parse('../xml_files/master_securebank_1.xml')
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
	print("SecureBank 1 ==> XML Generated")

	now = datetime.now()
	actual_time = str(now.strftime("%Y-%m-%d"))
	save_path = r'../generated_dag_files'
	complete_name = os.path.join(save_path, str(actual_time) + "_securebank_1.xml")
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

#tree.write("Dag Account - " + str(actual_time) + ".xml", xml_declaration=True)
#newDateArray[oldDate]
#print(newDateArray)
#Replace Old Date value with new Date Value
#tree[oldDate] = newDateArray[oldDate]

#Update XMLFile
updateXML(tree)


# for date in newDateArray:
#	  updatedDate = date # newDateArray[0]

#	  node.text = updatedDate # newDateArray[0]

# print(updatedDate) # newDateArray.last()

# for node in tree.findall('.//transDate'):
#	  node.text = date # Please note it has to be str '2015', not int like 2015
#	  #print(node.text)
#return None


#postTest(tree)
#balanceUpdater(tree)
#transactionAmountUpdater(tree)
#baseTypeRandomizer(tree)
#accountName(tree)
# postDateUpdater(tree)
#transDateUpdater(tree)
#print("XML File Created")
#print(newArray)
#updateXML(newDate(oldDate(tree)))
#newDate(oldDate(tree))
#oldDate(newDate(tree))

#finalDates = transUpdater(dateGetter(tree))
#dateGetter(dateArray)


#return

# for num in range(0, len(tree.findall('.//transDate'))):
#	  print(num)
#	  print(tree.findall('.//transDate')[num].text)
#	  tree.findall('.//transDate')[num].text = newDateArray[num]
#	  print(tree.findall('.//transDate')[num].text)
