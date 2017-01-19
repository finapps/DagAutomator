from time import gmtime, strftime
from datetime import datetime, timedelta
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random
import copy


# Open File to be modified
tree = ET.parse('user.xml')
root = tree.getroot()

for c in tree.iter('transaction'):
	dupe = copy.deepcopy(c)
	tree.append(dupe)
print tree

