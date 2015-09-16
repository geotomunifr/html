import time
from mod_python import Session

varTest=3

def getVarTest(req):
	req.content_type = 'text/plain'
	req.write('varTest=%d'%varTest)

def method(req):
	req.content_type = 'text/xml'
	req.write('<items><item>1</item><item>2</item></items>') # parserror!

def test(req):
	req.content_type = 'text/plain'
	req.write('Plain Text')

def eventSource(req):
	global varTest
	req.content_type = 'text/event-stream'
	number=0
	time.sleep(1)
	while(number<10):
		req.write("event:data\n");
		req.write('data:%s\n\n'%number)
		number=number+1
		time.sleep(1)
		varTest=varTest+1

def handler(req):
	session = Session.Session(req)

	try:
		session['hits'] += 1
	except:
		session['hits'] = 1

	session.save()
	req.content_type = 'text/plain'
	req.write('Hits asdf: %d\n' % session['hits'])
	
