import pysolr
import json
import sys

# Argument 1 the json line file to index
file_to_index = sys.argv[1]

# Argument 2 core to connect 
core_name = sys.argv[2]

solr = pysolr.Solr('http://localhost:8983/solr/%s/' % core_name)

with open(file_to_index) as fil:
	for line in fil:
		json_obj = json.loads(line)
		query = json_obj['title'].replace('- Wikipedia','').replace(':',' ')
		results = solr.search('content:(%s)' % query, **{'fl': 'score,url',})
		print(query)
		for (i,result) in enumerate(results):
			print('\t', i, result)