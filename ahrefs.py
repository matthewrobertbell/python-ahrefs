import urllib2
import datetime
from collections import defaultdict
from lxml import etree

class ahrefs(object):
	def __init__(self,key):
		self.key = key
		self.namespace = 'http://ahrefs.com/schemas/api/%s/1'
		
	def request(self,request_url,timeout):
		response = urllib2.urlopen(request_url,timeout=timeout).read()
		return etree.XML(response)
		
	def parse_result(self,result,method_name):
		parsed_result = {}
		for child in result.iterchildren():
			text = child.text.strip()
			tag = child.tag.strip().replace('{'+self.namespace % method_name+'}','')
			if text.lower() in ('true','false'):
				text = text.lower() == 'true'
			if tag == 'visited':
				text = datetime.datetime.strptime(text,'%Y-%m-%dT%H:%M:%SZ')
			parsed_result[tag] = text
		for child in result.iterchildren():
			text = child.text.strip()
			tag = child.tag.strip().replace('{'+self.namespace % method_name+'}','')
			if text.lower() in ('true','false'):
				text = text.lower() == 'true'
			if tag == 'visited':
				text = datetime.datetime.strptime(text,'%Y-%m-%dT%H:%M:%SZ')
			if isinstance(text,basestring):
				if '.' in text:
					try:
						text = float(text)
					except:
						pass
				else:
					try:
						text = int(text)
					except:
						pass
			parsed_result[tag] = text
		return parsed_result
		
	def filter_date(self,parsed_result,filter_date_newer,filter_date_older):
		if filter_date_newer:
			if isinstance(filter_date_newer,int):
				filter_date = datetime.timedelta(days=filter_date)
			if datetime.date.today() - filter_date_newer > parsed_result['visited']:
				return False
		if filter_date_older:
			if isinstance(filter_date_older,int):
				filter_date = datetime.timedelta(days=filter_date)
			if datetime.date.today() - filter_date_older < parsed_result['visited']:
				return False
		return True
		
		
	def links(self,target,mode='exact',internal=False,count=1000,timeout=30,filter_nofollow=None,filter_link_type=None,filter_date_newer=None,filter_date_older=None,simple_results=True):
		method_name = 'links'
		request_url = 'http://ahrefs.com/api.php?AhrefsKey=%s&type=inlinks&mode=%s&include_internal=%s&count=%s&target=%s' % (self.key,mode,str(internal).lower(),count,target)
		response = self.request(request_url,timeout)
		results = defaultdict(list)
		for result in response.xpath('//n:result',namespaces={'n': self.namespace % method_name}):
			parsed_result = self.parse_result(result,method_name)
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
			if not self.filter_date(parsed_result,filter_date_newer,filter_date_older):
				break
			results[parsed_result['destination_url']].append(parsed_result)
		if simple_results:
			new_results = []
			for v in results.values():
				for result in v:
					new_results.append(result)
			return new_results
		return results
		
	def pages(self,target,mode='domain',count=1000,timeout=30,filter_date_newer=None,filter_date_older=None,filter_http_code=None,filter_http_code_include=False,filter_size_larger=None,filter_size_smaller=None):
		method_name = 'pages'
		request_url = 'http://ahrefs.com/api.php?AhrefsKey=%s&type=pages&count=%s&mode=%s&target=%s' % (self.key,count,mode,target)
		response = self.request(request_url,timeout)
		results = []
		if filter_http_code:
			filter_http_code = [int(code) for code in filter_http_code]
		for result in response.xpath('//n:result',namespaces={'n': self.namespace % method_name}):
			parsed_result = self.parse_result(result,method_name)
			if not self.filter_date(parsed_result,filter_date_newer,filter_date_older):
				break
			if filter_http_code:
				if filter_http_code_include and parsed_result['http_code'] not in filter_http_code:
					break
				if not filter_http_code_include and parsed_result['http_code'] in filter_http_code:
					break
			if filter_size_larger:
				if parsed_result['size'] > filter_size_larger:
					break
			if filter_size_smaller:
				if parsed_result['size'] < filter_size_smaller:
					break
			results.append(parsed_result)
		return results
			
