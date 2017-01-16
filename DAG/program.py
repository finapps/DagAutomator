import xml.etree.ElementTree as ET
from time import gmtime, strftime
import random
from datetime import datetime, timedelta
import dateutil.parser


# Open File to be modified
tree = ET.parse('user.xml')
root = tree.getroot()

# Parser to Change ISOFormat to Date Object
def getDateTimeFromISO8601String(i):
	d = dateutil.parser.parse(i)
	return d

#Date Optimizer
def dateUpdate(xmlFile):
	for dates in root.iter('transDate'):
		originalDate = dates.text
		newDate = getDateTimeFromISO8601String(originalDate)
		changedDate = newDate - timedelta(days=90)
		dates = changedDate.isoformat()
	return dates

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



balanceUpdater(tree)
transactionAmountUpdater(tree)
baseTypeRandomizer(tree)
accountName(tree)
dateUpdate(tree)
#print accountName(tree).text
   
# Write back to a file
now = datetime.now()
actual_time = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
tree.write("Dag Account - " + str(actual_time) + ".xml", xml_declaration=True)

