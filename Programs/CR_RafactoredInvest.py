import xml.etree.ElementTree as ET
from time import strftime
import datetime as dt
import dateutil.parser, dateutil.relativedelta
import random
from googlefinance import getQuotes
import json

#Variables
datesArray = []
balanceArray = []
valueArray = []
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
	return transDates

def getStockPrice(xmlFile):
	holdings = tree.iter('holding')
	for holdings in tree.iter('holding'):
		price = float(holdings.find('price').text)
		symbol = holdings.find('symbol').text
		tickerData = json.dumps(getQuotes(symbol), indent=2)
		resp_dict = json.loads(tickerData)
		lastPrice = resp_dict[0]['LastTradePrice']
		print(lastPrice)
		for price in holdings.iter('price'):
			new_price = lastPrice	
	return price


def balanceSumModule(xmlFile):
	transactions = tree.iter('holding')
	for value in transactions:
		symbol = value.find('symbol').text
		quantity = float(value.find('quantity').text)
		tickerData = json.dumps(getQuotes(symbol), indent=2)
		resp_dict = json.loads(tickerData)
		lastPrice = resp_dict[0]['LastTradePrice']
		quantityPrice = lastPrice
		individual_balance = quantity * float(quantityPrice)
		balanceArray.append(individual_balance)
		updateValue(balanceArray)
		total_balance = balanceArray
		final_balance = str(sum(total_balance))
		#print("Total Balance:" + str(final_balance))
	for node in tree.iter('balance'):
		balType = node.attrib.get('balType')
		if balType == 'totalBalance':
			current_amount = node.find('curAmt')
			current_amount.text = str(final_balance)
	return value.text, current_amount

# def updateValue(xmlFile):
# 	holdings = tree.iter('holding')
# 	for holdings in tree.iter('holding'):
# 		price = float(holdings.find('price').text)
# 		quantity = float(holdings.find('quantity').text)
# 		symbol = holdings.find('symbol').text
# 		tickerData = json.dumps(getQuotes(symbol), indent=2)
# 		resp_dict = json.loads(tickerData)
# 		lastPrice = resp_dict[0]['LastTradePrice']
# 		individual_balance = quantity * float(lastPrice)
# 		for value in holdings.iter('value'):
# 			value.text = individual_balance
# 			value = str(value.text)
# 			print(value)
# 		return value

def balanceSumModule(xmlFile):
	transactions = tree.iter('holding')
	for value in transactions:
		symbol = value.find('symbol').text
		quantity = float(value.find('quantity').text)
		tickerData = json.dumps(getQuotes(symbol), indent=2)
		resp_dict = json.loads(tickerData)
		lastPrice = resp_dict[0]['LastTradePrice']
		quantityPrice = lastPrice
		individual_balance = quantity * float(quantityPrice)
		balanceArray.append(individual_balance)
		total_balance = balanceArray
		final_balance = str(sum(total_balance))
		print("Total Balance:" + str(final_balance))
	for node in tree.iter('balance'):
		balType = node.attrib.get('balType')
		if balType == 'totalBalance':
			current_amount = node.find('curAmt')
			current_amount.text = str(final_balance)
	return value.text, current_amount

def getAllData(xmlFile):
	holdings = tree.iter('holding')
	for holdings in tree.iter('holding'):
		price = float(holdings.find('price').text)
		quantity = float(holdings.find('quantity').text)
		symbol = holdings.find('symbol').text
		value = holdings.find('value').text
		tickerData = json.dumps(getQuotes(symbol), indent=2)
		resp_dict = json.loads(tickerData)
		lastPrice = resp_dict[0]['LastTradePrice']
		individual_balance = quantity * float(lastPrice)
		holdings.text = updateValue(individual_balance)
	return holdings





#getAllData(tree)
getStockPrice(tree)
updateXML(tree)
balanceSumModule(tree)
#updateValue(tree)


# Write back to a file
now = dt.datetime.now()
actual_time = str(now.strftime("%Y-%m-%d-%M"))
tree.write(str(actual_time) + "_investment_1.xml", xml_declaration=True)
