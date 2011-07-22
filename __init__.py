from ahrefs import *

if __name__ == '__main__':
	obj = ahrefs('fakekey')
	print obj.pages('http://www.reddit.com/')
