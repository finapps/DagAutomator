from time import gmtime, strftime
from datetime import datetime, timedelta as dt
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random

# Global Variables
global updatedDate

# Open File to be modified
tree = ET.parse('user.xml')
root = tree
datesArray = []

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
  for dates in root.iter('transDate'):
    originalDate = dates.text
    todayDate = datetime.now()
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

    '''
     *** USE ONLY IF WE WANT TO SET A RANGE AND MOST ALL TRANSACTIONS INTO THAT RANGE ****
    
    if (transactionDate > beginDate and transactionDate < todayDate):
      dates.text = str(transactionDate.isoformat())
    else:
      updatedDate = abs((todayDate - youngest).days)
      newDates = transactionDate + dateutil.relativedelta.relativedelta(days=updatedDate)
      dates.text = str(newDates.isoformat())
    '''
  return dates
  



  
'''
# Randomizer for account Name
def accountName(xmlFile):
  for accountNames in root.iter('accountName'):
    accountName = ["Chase Checking","Wells Fargo Checking", "Merrill Lynch"]
    new_accountName = random.choice(accountName)
    accountNames.text = str(new_accountName)
  return accountNames

# Randomly chooses credit of debit between each transaction
def baseTypeRandomizer(xmlFile):
  for i in root.iter('transaction'):
    baseType = ["credit","debit"]
    i.attrib["baseType"] = random.choice(baseType)
  return i.text

# Randomizer for balance
def balanceUpdater(xmlFile):
  for balance in root.iter('curAmt'):
    new_balance = round(random.uniform(2000.0, 100000.0), 2)
    balance.text = str(new_balance)
    #print('Balance Amount Updated')
  return balance

# Randomize amounts for each transaction
def transactionAmountUpdater(xmlFile):
  # Updates amounts on each transaction
  for amt in root.iter('amount'):
    amount = round(random.uniform(1.0, 10000.0), 2)
    amt.text = str(amount)
  return amount
'''


#balanceUpdater(tree)
#transactionAmountUpdater(tree)
#baseTypeRandomizer(tree)
#accountName(tree)
dateUpdater(tree)


# Write back to a file
now = datetime.now()
actual_time = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
tree.write("Checking Dag Account - " + str(actual_time) + ".xml", xml_declaration=True)
