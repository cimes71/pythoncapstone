import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import sqlite3


import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('inmatedb.sqlite')
cur = conn.cursor()

#url = "http://www.tdcj.state.tx.us/death_row/dr_info/medinajavierlast   .html"

cur.execute('SELECT ID, lasturl FROM Inmateinfo')
lst = list()
for row in cur :

    try:
        inmate = row[0]
        url = row[1]
        count = 0
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        para = soup.findAll("p")
        for p in para:
            line = p.getText()
            y = re.findall(r'(?i)(sorry|forgive|remorse|apologize)', line)
            if len(y) > 0:
                count = count + len(y)
                #print(y)
        if count > 0:
            print(str(inmate))
            newtup = (inmate, count)
            lst.append(newtup)
            #cur.execute('''UPDATE Inmateinfo SET wordcount = ? where ID = ? ''',(count, inmate))
            #conn.commit()
    except:
         print("Exception")

for inmate, count in lst:
    cur.execute('''UPDATE Inmateinfo SET wordcount = ? where ID = ? ''',(count, inmate))
    print(inmate, count)
conn.commit()
cur.close()
