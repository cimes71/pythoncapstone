import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re


import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "http://www.tdcj.state.tx.us/death_row/dr_info/medinajavierlast.html"

try:
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    para = soup.findAll("p")
    count = 0
    for p in para:
        if count > 4:
            line = p.getText()
            print(line)
        count = count + 1


except:
   print("Exception")
