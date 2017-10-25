import pysolr
import json
import sys

# Argument 1 the json line file to index
file_to_index = sys.argv[1]

# Argument 2 core to connect 
core_name = sys.argv[2]

solr = pysolr.Solr('http://localhost:8983/solr/%s/' % core_name)

count = 0

recip_rank = []

with open(file_to_index) as fil:
	for line in fil:
		json_obj = json.loads(line)
		anwser = json_obj['url']
		query = json_obj['title'].replace('- Wikipedia','')
		query = query.replace(':',' ')
		results = solr.search('content:(%s)' % query, **{'fl': 'score,url',})
		notFound = False
		for (i,result) in enumerate(results):
			if anwser == result['url'][0]:
				rr = 1./(i+1.)
				recip_rank.append(rr)
				notFound = False
				break
			notFound = True
		if notFound:
			 recip_rank.append(0.)
		count += 1
	print("\r%d" % count, "RR: %.2f" % (sum(recip_rank)/len(recip_rank)) )