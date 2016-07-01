import urllib
import sqlite3
import json
import time
import ssl


#If using in China, use this serviceurl = "http://maps.google.cn/maps/api/geocode/json?"
serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"

scontext = None

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')
fh = open("geotrackerdata.txt")
count = 0
for line in fh:
    if count > 200 : break
    address = line.split(',')
    if address[2] and address[3] and address[4] == 'null':
        continue #excluding nulls. We don't want unresolved coordinates
    print address[2], address[3], address[4]
    addressString = address[2] + " " + address[3] + " " + address[4]
    print addressString

    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (buffer(addressString), ))
    try:
      data = cur.fetchone()[0]
      print "Found in database ", addressString
      continue
    except:
      pass

      print 'Resolving', addressString
      url = serviceurl + urllib.urlencode({"sensor":"false", "address": addressString})
      print 'Retrieving', url
      uh = urllib.urlopen(url, context=scontext)
      data = uh.read()
      print 'Retrieved',len(data),'characters',data[:20].replace('\n',' ')
      count = count + 1
      try:
          js = json.loads(str(data))
      except:
          continue
      if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
          print "========================="
          print "   Failure To Retrieve"
          print "========================="
          print data
          break
      cur.execute('''INSERT INTO Locations (address, geodata)
      VALUES ( ?, ? )''', ( buffer(addressString),buffer(data) ) )
      conn.commit()
      time.sleep(1)

print "===================="
print " RUN GEODUMP.PY NOW "
print "===================="
