import subprocess
import time
import posix_ipc
from mod_python import Session


def mesureVoltage(req):
	session = Session.Session(req)
	req.content_type = 'text/plain'
	req.write("voltage");
	# req.wiret(dir(req));
	geotomCmd=posix_ipc.MessageQueue('/geotom_cmd');
	geotomCmd.send(req.form.getfirst('func'))
	geotomCmd.close()

def geotomEvent(req):
	global varTest
	req.content_type = 'text/event-stream'
	msg="init"
	geotomRsp=posix_ipc.MessageQueue('/geotom_rsp');
	while(1):
		req.write("event:data\n");
		req.write('data:%s\n\n'%msg)
		msg=geotomRsp.receive()[0]

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

def geotomOn():
	gpio_f = open('/sys/class/gpio/gpio49/value', 'w')
	gpio_f.write('1\n');
	gpio_f.close();


def geotomOff():
	gpio_f = open('/sys/class/gpio/gpio49/value', 'w')
	gpio_f.write('0\n');
	gpio_f.close();

def geotomSetGPIO(gpio,on):
	gpio_f = open('/sys/class/gpio/gpio%d/value'%gpio, 'w')
	if(on):
		gpio_f.write('1\n');
	else:
		gpio_f.write('0\n');
	gpio_f.close();

	
