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
def dateUpdater(xmlFile):
  for dates in root.iter('date'):
    originalDate = dates.text
    todayDate = dt.datetime.now()
    #Sets the transactions range 3 months
    #beginDate = todayDate + dateutil.relativedelta.relativedelta(months=-3)
    transactionDate = getDateTimeFromISO8601String(originalDate)
    #Add all transactions into an array.
    datesArray.append(transactionDate)
    newArray = datesArray
    #Find the Youngest Date (most recent)
    youngest = max(dt for dt in newArray if dt < todayDate)
    updatedDate = abs((todayDate - youngest).days)
    newDates = transactionDate + dateutil.relativedelta.relativedelta(days=updatedDate)
    dates.text = str(newDates.isoformat())
    # * Uncomment to Test
    #testModule(updatedDate, youngest, todayDate)
    return dates

def balanceSumModule(xmlFile):
    transactions = tree.iter('holding')
    for value in transactions:
        symbol = value.find('symbol').text
        quantity = float(value.find('quantity').text)
        tickerData = json.dumps(getQuotes(symbol), indent=2)
        resp_dict = json.loads(tickerData)
        lastPrice = resp_dict[0]['LastTradePrice']
        quantityPrice = float(lastPrice)
        print(quantity, symbol, quantityPrice)
        individual_balance = quantity * quantityPrice
        print(individual_balance)
        balanceArray.append(individual_balance)
        total_balance = balanceArray
        final_balance = str(sum(total_balance))
        print("Total Balance:" + str(final_balance))


    #Update balance
    for node in tree.iter('balance'):
        balType = node.attrib.get('balType')
        if balType == 'totalBalance':
            current_amount = node.find('curAmt')
            current_amount.text = str(final_balance)
        return value.text, current_amount

# Console TESTING Module #
def testModule(dayDiff, youngest, today):
    print ("\nToday's Date: " + str(today) + "\n")
    print ("Most Recent Transaction Date: " + str(youngest) + "\n")
    print ("Day Difference: " + str(dayDiff) + "\n")
    return (dayDiff, youngest, today)


dateUpdater(tree)
balanceSumModule(tree)

# Write back to a file
now = dt.datetime.now()
actual_time = str(now.strftime("%Y-%m-%d"))
tree.write(str(actual_time) + "_investment_1.xml", xml_declaration=True)