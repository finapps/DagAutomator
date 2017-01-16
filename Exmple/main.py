import random
import datetime
import xml.etree.ElementTree as ET
from time import gmtime, strftime


#Read in the XML file so it can be manipulated
tree = ET.parse('books.xml')
root = tree.getroot()


# Get the Total Number of Elements in the XML file
result = len(root.getchildren())
print(result)



#iterate though rank and update
for rank in root.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
   # rank.set('updated', 'yes')
    

# Randomly create new price range.    
for price in root.iter('price'):
    new_price = round(random.uniform(2.0, 2000.0), 2)
    price.text = str(new_price)
    #price.set('new price', 'yes')
    



    



 # Insert a new element after <book>...</book>




# Write back to a file
now = datetime.datetime.now()
actual_time = str(now.strftime("%Y-%m-%d-%H-%M"))
tree.write("TestFile - " + str(actual_time) + ".txt", xml_declaration=True)