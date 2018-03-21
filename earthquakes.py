# 
# Example file for parsing and processing JSON
# (For Python 3.x, be sure to use the ExampleSnippets3.txt file)

import tkinter
import urllib.request
import json
import operator
import datetime
from datetime import date, time

def printResults(data):
  eq_table =  []
  sp = 0
  ca = 0
  # sorted_table = []
  tuple_table = ()
  # Use the json module to load the string data into a dictionary
  try:
     theJSON = json.loads(data)
     num = theJSON["metadata"]["count"]

  except :
    print("Unable to access JSON data. Possible no internet connection ")
    return

  # now we can access the contents of the JSON like any other Python object
  if "title" in theJSON["metadata"]:
    print (str(theJSON["metadata"]["count"]) + " earthquakes today " + str(datetime.datetime.now()))

    # tuple_table = (theJSON["features"]["place"],theJSON["features"]["mag"],theJSON["features"]["felt"])
    # tuple_table = ("scott", "barth")
    # create the table columns in a list
    for i in theJSON["features"]:
        eq_table.append([i["properties"]["place"],i["properties"]["mag"],i["properties"]["felt"]])

        # count the soda springs quakes
        if "Soda Springs, Idaho" in  i["properties"]["place"]:
          sp = sp + 1
        if "California" in  i["properties"]["place"]:
          ca +=1

        #
      # sort the table my magnitude

    sorted_table =  sorted(eq_table, key=operator.itemgetter(1))


    print ("| Where earthquake occured                                     | Mag | Times felt")
    print ("----------------------------------------------------------------------------")
    for item in sorted_table:
        print("| " + item[0] + " "*(60-len(item[0])), "|", "%2.1f" %(item[1]) + " |" + str(item[2]) )
    print("Total Soda Springs Quakes: {} ".format(sp))
    print("Total California Quakes: {} ".format(ca))

  else: 
    print ("no data")
     # print only the events where at least 1 person reported feeling something
  
#   for i in theJSON["features"]:
#       feltReports = i["properties"]["felt"]
#       if (feltReports != None) & (feltReports > 0):
#           print "%2.1f" % i["properties"]["mag"], i["properties"]["place"], " reported " + str(feltReports) + " times"
#             
#   print str(len(aTable)) + " over 4.0"        
#   for i in od:
#     print i, od
#     list(sorted(aTable.keys()))        
     
#     print place

#             print str(i["properties"]["mag"]) + " - "  + i["properties"]["place"] 
     
  
def main():
  # define a variable to hold the source URL
  # In this case we'll use the free data feed from the USGS
  # This feed lists all earthquakes for the last day larger than Mag 2.5


  urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
    # read the data from the URL and print it
  webResp = urllib.request.urlopen(urlData)

  if (webResp.getcode() == 200):
      data = webResp.read()
      printResults(data)




      
   
  
  

#   printResults(data)
  

if __name__ == "__main__":
  main()
