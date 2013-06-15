import time
import MySQLdb as mdb
import json


con = mdb.connect("localhost",
	"root", "password", "cookies")

cur = con.cursor(mdb.cursors.DictCursor)
cur.execute("select * from domains")

row = cur.fetchall()

i = 0

data = []

for r in row:
	url = r['url']

	cur.execute("select * from cookies where domain_id=%s", (r['id']))

	cookies = cur.fetchall()

	offending = []
	tall = []

	mapping = {'__utmz': 'Google Analytics',
	'__utmc':'Google Analytics',
	'__utma':'Google Analytics',
	'__utmb':'Google Analytics',
	'phpAds_geoInfo': 'OpenX Ads',
	'phpAds_id': 'OpenX Ads',
	'__gads':'Google Ads'}


	for c in cookies:
		if c['name'] in mapping:
			found = False
			for x in offending:
				if x == mapping[c['name']]:
					found = True

			if not found:
				offending.append(mapping[c['name']])
		else:
			tall.append(c['name'])

	i=i+1

	data.append({'id':i, 'url': url, 'cookies': len(cookies), 'other': tall, 'offending':offending})

template = open('template.html', 'r')

html = template.read()

html=html.replace('/* ===HERE COMES DATA=== */', json.dumps(data))

f = open('index.html', 'w')
f.write(html)
f.close()