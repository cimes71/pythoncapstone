import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import sqlite3

import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html"

html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")
baselink = "http://www.tdcj.state.tx.us/death_row/"

conn = sqlite3.connect('inmatedb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Inmateinfo')

cur.execute('''
CREATE TABLE Inmateinfo(ID INT, lastname TEXT, firstname TEXT, race TEXT, executiondate DATE, lasturl TEXT, lastwords TEXT, wordcount INT)''')


table = soup.find("table", { "class" : "tdcj_table indent" })
rows = table.find_all('tr')
count = 0
statement = ''
for tr in rows:
    cols = tr.findAll('td')
    #print (len(cell))
    try:
        inmateid = cols[0].text.strip()
        lastname = cols[3].text.replace(",", "")
        firstname = cols[4].text.strip(', ')
        execdate = cols[7].text.strip()
        race = cols[8].text.strip()
        link = cols[2].a['href']
        fulllink = baselink + link
        print(lastname.strip() + " " + firstname.strip() + " " + execdate + " " + fulllink)
        cur.execute('''INSERT INTO Inmateinfo (ID, lastname, firstname, race, executiondate, lasturl, lastwords, wordcount)
                VALUES (?,?, ?, ?, ?, ?,?,?)''', (inmateid, lastname,firstname, race, execdate, fulllink, statement, count))


    except:
        print("Exception")
conn.commit()
cur.close()
