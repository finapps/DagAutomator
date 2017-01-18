from time import gmtime, strftime
from datetime import datetime, timedelta
import dateutil.parser, dateutil.relativedelta
import xml.etree.ElementTree as ET
import random
import copy


# Open File to be modified
tree = ET.parse('user.xml')
root = tree.getroot()


print("THIS d3dLINE THERE")

def textMethod(xmlFile):
	for child in root:
		for subchild in child:
			link = subchild.find('transaction')
			for grandchild in subchild.findall('.//transaction'):
				
				dupe = copy.deepcopy(grandchild)
				new = link.append(dupe)
				return(new)


textMethod(tree)

now = datetime.now()
actual_time = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
tree.write("Dag Account - " + str(actual_time) + ".xml", xml_declaration=True)