import json
from pprint import pprint

with open('problems.json') as data_file:    
    data = json.load(data_file)

print('site, contestId, score, name, solvedCount, link, tags')
site = 'codeforces.com'
score = 0
statistic = dict()

#Problems statistic

for x in data['result']['problemStatistics']:
	statistic[(x['contestId'], x['index'])] = x['solvedCount']

for x in data['result']['problems']:	
	contestId = x['contestId']
	try:
		score = int(x['points'])
	except:
		score = 0
	name = x['name']
	try:
		name = name.encode('ascii')		
	except:
		continue
	solvedCount = statistic[(contestId, x['index'])]
	link = 'http://codeforces.com/problemset/problem/{0}/{1}'.format(contestId, x['index'])
	print ','.join([site, str(contestId), str(score), "\"" + name + "\"", str(solvedCount), link]) + ',' + repr([str(u) for u in x['tags']])
	
	