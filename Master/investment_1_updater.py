import xml.etree.ElementTree as ET
from time import strftime
import datetime as dt
import dateutil.parser, dateutil.relativedelta
import random
#from googlefinance import getQuotes
import json
import os.path
import boto3

#Variables
datesArray = []
balanceArray = []
s3 = boto3.client('s3')

# Open File to be modified
tree = ET.parse('master_invest_1.xml')
root = tree

# Parser to convert date from ISOFormat to Date Object
# This allows us to manipulate the date range.
def getDateTimeFromISO8601String(i):
	d = dateutil.parser.parse(i)
	return d
'''
 Compare current day with youngest(most recent) transaction date.
 Calculate the difference between the two days and update all other transactions
 exactly that many days.
'''
def oldDate(xmlFile):
	transactions = tree.iter('transaction')
	for transaction in transactions:
		transDate = transaction.find('date').text
		transactionDate = getDateTimeFromISO8601String(transDate)
		datesArray.append(transactionDate)
		newArray = datesArray
	return newArray

def newDate(newArray):
	newDateArray = []
	for date in newArray:
		youngest_date = max(newArray)
		todayDate = dt.datetime.now()
		dateDiff = abs((todayDate - youngest_date).days)
		newDate = date + dateutil.relativedelta.relativedelta(days=dateDiff)
		date = str(newDate.isoformat())
		newDateArray.append(date)
	return newDateArray

def updateXML(xmlFile):
	originalDatesArr = oldDate(xmlFile)
	adjustedDatesArr = newDate(originalDatesArr)
	transDates = xmlFile.findall('.//date')
	for num in range(0, len(transDates)):
		transDates[num].text = adjustedDatesArr[num]
	#Write back to a file
	print("Investment 1 ==> XML Generated")
	return transDates

#def getStockPrice(xmlFile):
#	for holdings in tree.iter('holding'):
#		price = float(holdings.find('price').text)
#		symbol = holdings.find('symbol').text
#		tickerData = json.dumps(getQuotes(symbol), indent=2)
#		resp_dict = json.loads(tickerData)
#		lastPrice = resp_dict[0]['LastTradePrice']
#		for price in holdings.iter('price'):
#			#print(price)
#			new_price = lastPrice
#			price.text = str(new_price)
#			#print(price.text)
#
#	return price


#def balanceSumModule(xmlFile):
#	transactions = tree.iter('holding')
#	for value in transactions:
#		symbol = value.find('symbol').text
#		quantity = float(value.find('quantity').text)
#		tickerData = json.dumps(getQuotes(symbol), indent=2)
#		resp_dict = json.loads(tickerData)
#		lastPrice = resp_dict[0]['LastTradePrice']
#		quantityPrice = lastPrice
#		print(quantityPrice)
#		print(quantity, symbol, quantityPrice)
#		individual_balance = quantity * float(str(quantityPrice).replace(',',''))
#		print(individual_balance)
#		balanceArray.append(individual_balance)
#		total_balance = balanceArray
#		final_balance = str(sum(total_balance))
#		print("Total Balance:" + str(final_balance))


	#Update balance
	# for node in tree.iter('balance'):
	# 	balType = node.attrib.get('balType')
	# 	if balType == 'totalBalance':
	# 		current_amount = node.find('curAmt')
	# 		current_amount.text = str(final_balance)

	#Update the value of each holding
#def updateValue(xmlFIle):
#	for holdings in tree.iter('holding'):
#		price = float(holdings.find('price').text.replace(',',''))
#		quantity = float(holdings.find('quantity').text)
#		symbol = holdings.find('symbol').text
		#value = holdings.find('value').text

		#print(value)
#		tickerData = json.dumps(getQuotes(symbol), indent=2)
##		lastPrice = resp_dict[0][10.00]
#		individual_balance = quantity * float(lastPrice.replace(',',''))
#		for value in holdings.iter('value'):
#			value.text = individual_balance
#			value.text = str(value.text)
#		print(value.text)
#	return value


# # Console TESTING Module #
# def testModule(dayDiff, youngest, today):
#	  print ("\nToday's Date: " + str(today) + "\n")
#	  print ("Most Recent Transaction Date: " + str(youngest) + "\n")
#	  print ("Day Difference: " + str(dayDiff) + "\n")
#	  return (dayDiff, youngest, today)

#getStockPrice(tree)
updateXML(tree)
#balanceSumModule(tree)
#updateValue(tree)

# Write back to a file
now = dt.datetime.now()
actual_time = str(now.strftime("%Y-%m-%d"))
save_path = r'generated_dag_files'
complete_name = os.path.join(save_path, str(actual_time) + "_investment_1.xml")
tree.write(complete_name, xml_declaration=True)
filename = complete_name
bucket_name = 'dagautomator'
s3.upload_file(filename, bucket_name, filename)

