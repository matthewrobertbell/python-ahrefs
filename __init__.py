import requests
import json
import urllib

MODES = ['domain', 'subdomains', 'prefix', 'exact']

class ahrefs(object):
	def __init__(self,key):
		self.key = key
		
	def request(self, method_name, **kwargs):
		if 'mode' in kwargs and kwargs['mode'] not in MODES:
			raise Exception('Mode must be one of: '+', '.join(MODES))
		kwargs['output'] = 'json'
		kwargs['AhrefsKey'] = self.key
		options = '&'.join([k+'='+urllib.quote_plus(str(v)) for k,v in kwargs.items()])
		request_url = 'http://api.ahrefs.com/{method_name}.php?{options}'.format(method_name=method_name, options=options)
		response = requests.get(request_url)
		return json.loads(response.content)

	def backlinks(self, target, count=100, mode=MODES[0]):
		return self.request(method_name='get_backlinks', target=target, count=count, mode=mode)

	def api_units_left(self):
		return self.request(method_name='get_units_left')