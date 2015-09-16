import subprocess
import time
import posix_ipc
import socket
#from mod_python import Session



def mesureVoltage(req):

	#session = Session.Session(req)
	req.content_type = 'text/plain'	
	s = socket.socket()
	s.connect(('localhost', 5000))
	s.send(req.form.getfirst('func')+'\n');
	s.close()
	#geotomCmd.send(req.form.getfirst('func'))


def geotomEvent(req):

	req.content_type = 'text/event-stream'
	s = socket.socket()
	try:
		s.connect(('localhost', 5000))
	except:
		req.write("event:data\n");
		req.write('data:{"msg": "Cannot connect to Geotom Programmm", "type": "error"}\n\n'%line)
		return 
	#s.send('Hello world!\n')
	data=""
	try:
		while True:
			newData=s.recv(1024)
			if newData=='':
				time.sleep(0.2)
			data =data+newData

			data=data.replace("\r", "")
			if data and data.endswith("\n"):
				for line in data.split("\n"):
					if line!='':
						req.write("event:data\n");
						req.write('data:%s\n\n'%line) 
				data=""
	except:
		req.write("event:data\n");
		req.write('data:{"msg": "Geotom disconnected", "type": "error"}\n\n'%line)
		return 

def geotomGetGPIO(gpio):
	gpio_f = open('/sys/class/gpio/gpio%d/value'%gpio, 'r')
	retval=False;
	gpioStateVal=gpio_f.read();
	if(gpioStateVal=='1\n'):
		retval=True;
	elif(gpioStateVal=='0\n'):
		retval=False;
	gpio_f.close();
	return retval;

def geotomSetGPIO(gpio,on):
	gpio_f = open('/sys/class/gpio/gpio%d/value'%gpio, 'w')
	if(on):
		gpio_f.write('1\n');
	else:
		gpio_f.write('0\n');
	gpio_f.close();

	
