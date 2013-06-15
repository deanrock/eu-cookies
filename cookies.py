from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import MySQLdb as mdb
import json

def check_cookies(url):
	con = mdb.connect("localhost",
		"root", "password", "cookies")
	cur=con.cursor()

	browser = webdriver.Firefox() # Get local session of firefox
	browser.delete_all_cookies()
	browser.get(url) # Load page

	cookies = browser.get_cookies()

	cur.execute("insert into domains (url, `datetime`) values (%s,  NOW())", (
		url))

	con.commit()

	domain = cur.lastrowid

	for c in cookies:
		cur.execute("insert into cookies (domain_id, name,domain,value) values (%s, %s, %s, %s)", (
		domain, c['name'], c['domain'], c['value']))
		con.commit()

	

	browser.close()

#check_cookies("http://www.24ur.com")

url = 'http://www.moss-soz.si/si/rezultati_moss/obdobje/default.html'

import re
import urllib, urllib2
f = urllib.urlopen(url)
content = f.read()

x = re.findall('<strong>(.*)<\/strong>', content)

y = x[:-1]

i = 0

for x in y:
	x = x.split('<')
	
	i = i+1
	print "%d. %s" % (i, x[0])
	check_cookies('http://'+str(x[0]))

"""assert "Yahoo!" in browser.title
elem = browser.find_element_by_name("p") # Find the query box
elem.send_keys("seleniumhq" + Keys.RETURN)
time.sleep(0.2) # Let the page load, will be added to the API
print browser.get_cookies()
try:
    browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
except NoSuchElementException:
    assert 0, "can't find seleniumhq"

"""