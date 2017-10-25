import pysolr
import json
import sys

# Argument 1 the json line file to index
file_to_index = sys.argv[1]

# Argument 2 core to connect 
core_name = sys.argv[2]

solr = pysolr.Solr('http://localhost:8983/solr/%s/' % core_name)

size_buffer = 1000
buffer_obj = []
count = 0
with open(file_to_index) as fil:
	for line in fil:
		json_obj = json.loads(line)
		json_obj['id'] = json_obj['url']
		buffer_obj.append(json_obj)
		if len(buffer_obj) == size_buffer:
			solr.add(buffer_obj)
			buffer_obj = []
		print("\r%d" % count, end='')
		count += 1
	solr.commit()
	print("\r%d" % count)