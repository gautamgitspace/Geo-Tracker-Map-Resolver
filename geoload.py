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
