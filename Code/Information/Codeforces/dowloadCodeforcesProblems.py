import requests
from BeautifulSoup import BeautifulSoup

getProblem = requests.get('http://codeforces.com/api/problemset.problems/')
getProblem = BeautifulSoup(getProblem.text)

s = getProblem.text

with open('problems.json','w') as f:
	print f.write(s.encode('utf-8'))
