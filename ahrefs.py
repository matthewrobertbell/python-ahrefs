import urllib2
import datetime
from collections import defaultdict
from lxml import etree

class ahrefs(object):
	def __init__(self,key):
		self.key = key
		self.namespace = 'http://ahrefs.com/schemas/api/links/1'
		
	def links(self,target,mode='exact',internal=False,count=1000,timeout=30,filter_nofollow=None,filter_link_type=None,filter_date_newer=None,filter_date_older=None):
		request_url = 'http://ahrefs.com/api.php?AhrefsKey=%s&type=inlinks&mode=%s&include_internal=%s&count=%s&target=%s' % (self.key,mode,str(internal).lower(),count,target)
		response = urllib2.urlopen(request_url,timeout=timeout).read()
		response_doc = etree.XML(response)
		results = defaultdict(list)
		
		for result in response_doc.xpath('//n:result',namespaces={'n': self.namespace}):
			parsed_result = {}
			for child in result.iterchildren():
				text = child.text.strip()
				tag = child.tag.strip().replace('{'+self.namespace+'}','')
				if text.lower() == 'false':
					text = False
				else:
					if text.lower() == 'true':
						text = True
				if tag == 'visited':
					text = datetime.datetime.strptime(text,'%Y-%m-%dT%H:%M:%SZ')
				parsed_result[tag] = text
			
			if filter_link_type:
				if parsed_result['link_type'] not in filter_link_type:
					break
			if filter_nofollow != None:
				if filter_nofollow:
					if not parsed_result['is_nofollow']:
						break
				else:
					if parsed_result['is_nofollow']:
						break
			if filter_date_newer:
				if isinstance(filter_date_newer,int):
					filter_date = datetime.timedelta(days=filter_date)
				if datetime.date.today() - filter_date_newer > parsed_result['visisted']:
					break
			if filter_date_older:
				if isinstance(filter_date_older,int):
					filter_date = datetime.timedelta(days=filter_date)
				if datetime.date.today() - filter_date_older < parsed_result['visisted']:
					break
			results[parsed_result['destination_url']].append(parsed_result)
		return results	
