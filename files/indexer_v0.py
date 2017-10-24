import pysolr
import json

file_to_index = "../../dataset/wiki_depth1.jl"
core_name = "wiki_core"
solr = pysolr.Solr('http://localhost:8983/solr/%s/' % core_name)

count = 0
with open(file_to_index) as fil:
	for line in fil:
		json_obj = json.loads(line)
		json_obj['id'] = json_obj['url']
		solr.add([json_obj])
		print("\r%d" % count, end='')
		count += 1
	print("\r%d" % count)