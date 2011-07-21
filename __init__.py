from ahrefs import *

if __name__ == '__main__':
	obj = ahrefs('fakekey')
	print obj.links('http://www.reddit.com/')
