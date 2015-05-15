import sys
import requests
from BeautifulSoup import BeautifulSoup

INF = 1000000

def getSuccesAttempts(data):
	tmpLink = 1

	for t in data.findAll('a'):
		if t.text == 'details':
			tmpLink = t
			break

	url = 'http://community.topcoder.com/' + tmpLink.get('href')
	response = requests.get(url)
	text = response.text
	data = BeautifulSoup(text)
	for t in data.findAll('td', {'class' : 'statText'}):
		if t.text == 'Problems Correct':
			tmpLink = t
	for i in xrange(12):
		tmpLink = tmpLink.nextSibling
	return int(tmpLink.text)


def show_inf(a):
	for x in dir(a):
		print x

def rev(s):
	b = list(s)
	b.reverse()
	return ''.join(b)

def getProblem(t):
#	print t
	a = t.findChildren('a')[0].get('href')
	a = rev(a)
	a = a[:a.find('=')]
	a = rev(a)
	return t.text, a

def getFullInf(data):
	tmpLink = 1
	cnt = -1
	for t in data.findAll('td', {'class' : 'statText'}):
		if cnt < 0:
			children = t.findChildren('a')
			fl = False
			for ch in children:
				if 'problem_statement' in ch.get('href'):
					fl = True
					break
			if fl:
				tmpLink = t			
				cnt = 0				
		if cnt < 0:
			continue
		cnt += 1
		if cnt > 5:
			break
		if cnt == 1:
			name, prLink = getProblem(t)
		elif cnt == 2:
			roundN, roundLink = getProblem(t)
		elif cnt == 5:
			tags = t.text

	return name, prLink, roundN, roundLink, tags	
			
print 'Problem Name, Problem Link {http://community.topcoder.com/stat?c=problem_statement&pm=}, Contest Name, Contest Link = {http://community.topcoder.com/stat?c=round_overview&rd=}, tags, solvedCount'

for problemId in xrange(1,INF):

	url = 'http://community.topcoder.com/tc?module=ProblemArchive&sr={0}&er={1}'.format(problemId, problemId)
	response = requests.get(url)
	text = response.text
	data = BeautifulSoup(text)
	End = True

	for t in data.findAll('a'):
		if t.text == 'details':
			End = False
			break
	if End:
		break
	success = getSuccesAttempts(data)
	nameProblem, problemLink, roundN, roundLink, tags = getFullInf(data)
	tags = '[' + tags + ']' 
	print (','.join(map(str, [nameProblem, problemLink, roundN, roundLink, tags, success])))