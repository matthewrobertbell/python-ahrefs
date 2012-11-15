import requests
import urllib
import os

MODES = ['domain', 'subdomains', 'prefix', 'exact']

class ahrefs(object):
	def __init__(self, key=None):
		self.key = key or os.environ.get('AHREFS_KEY')
		
	def request(self, method_name, **kwargs):
		if 'mode' in kwargs and kwargs['mode'] not in MODES:
			raise Exception('Mode must be one of: '+', '.join(MODES))
		kwargs['output'] = 'json'
		kwargs['AhrefsKey'] = self.key
		request_url = 'http://api.ahrefs.com/{method_name}.php'.format(method_name=method_name)
		return requests.get(request_url, params=kwargs).json

	def backlinks(self, target, count=100, mode=MODES[0]):
		return self.request(method_name='get_backlinks', target=target, count=count, mode=mode)

	def backlinks_count(self, target, mode=MODES[0]):
		return self.request(method_name='get_backlinks_count', target=target, mode=mode)

	def api_units_left(self):
		return self.request(method_name='get_units_left')

	def total_count_details(self, target, mode=MODES[0]):
		return self.request(method_name='get_ref_domains_ips_count', target=target, mode=mode)

	def crawled_pages(self, target, count=100, mode=MODES[0]):
		return self.request(method_name='get_pages', target=target, count=count, mode=mode)

	def anchors(self, target, count=100, mode=MODES[0]):
		return self.request(method_name='get_anchors_of_backlinks', target=target, count=count, mode=mode)

