import urllib2
from collections import defaultdict

class ahrefs(object):
	def __init__(self,key):
		self.key = key
		
	def links(self,target,mode=exact,internal=False,count=1000,timeout=30,filter_nofollow=None,filter_link_type=None):
		request_url = 'http://ahrefs.com/api.php?AhrefsKey=%s&type=inlinks&mode=%s&include_internal=%s&count=1000&target=%s' % (self.key,mode,str(internal).lower(),count,target)
		response = urllib2.urlopen(request_url,timeout=timeout).read()
		response_doc = etree.XML(response)
		results = {}
		
		for result in []:
			parsed_result = defaultdict(list)
			destination_url = result.xpath('destination_url').text()

			
			visited = datetime.datetime.strptime(result.xpath('visited').text(),'%Y-%m-%dT%H:%M:%SZ')
			
			results[destination_url].append(parsed_result)
		return results	
