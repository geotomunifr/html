from mod_python import apache

def index(req):

    req.content_type = "text/plain"
    req.write("Hello World!")

    return apache.OK

def simpleForm(req,firstname=""):
	req.content_type = 'text/html'
	req.write("""
	<!DOCTYPE html>
	<html>
	<body>
	<form>
	First name:<br>
	<input type="text" name="firstname" value="%s">
	<br>
	Last name:<br>
	<input type="text" name="lastname" value="Mouse">
	<br><br>
	<input type="submit" value="Submit">
	</form> 
	</body>
	</html>
	"""%firstname)

def gpio(req,enable="unknown"):
	
	req.content_type = 'text/html'

	gpio = open('/sys/class/gpio/gpio49/value', 'r+')

	gpioVal=int(gpio.read());
	actState="unknown";
	nextState="";
	


	if(enable=="OFF"):
		gpio.write('0\n');
		gpioVal=0
	elif(enable=="ON"):
		gpio.write('1\n');
		gpioVal=1
		
	if(gpioVal==1):
		nextState="OFF";
		actState="ON";
	elif(gpioVal==0):
		nextState="ON";
		actState="OFF";
	else:
		nextState="OFF";
		
		
	req.write("""
	<!DOCTYPE html>
	<html>
	<body>
	%d
	<form>
	Geotom is %s turn it
	<input type="submit" name="enable" value="%s">
	</form> 

	<form>
	<input type="submit" name="other" value="asdf">
	</form> 
	</body>
	</html>
	"""%(gpioVal,actState,nextState))
	
