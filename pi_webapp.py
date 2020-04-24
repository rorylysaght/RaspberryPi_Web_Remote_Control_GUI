# ######
#	Web Interface for Raspberry Pi 4 GPIO Control
# ######
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time, random
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define GPIO pins
pins = [12,20,16,21,8,23,24,25]
colors = ['red','green','blue','red','green','blue','orange','orange']
validColors = ['red', 'green', 'blue', 'orange']

# configure all pins for output
for i in pins:
	GPIO.setup(i, GPIO.OUT)

@app.route("/")
def index():
	# Read Sensors Status
	p = {}  #new dictionary
	for i in pins:
		p["P" + str(i)] = GPIO.input(i)

	return render_template('index.html', pinStatus=p, pins=pins, colors=colors)


@app.route("/<pinNum>/<action>")
def action(pinNum, action):
	pinNum = pinNum[1:] #strip off initial character "P"
	if pinNum.isdigit() == True:
	# if not targeting a specific pin, variable passed will be P99
		pinNum = int(pinNum)
	else: # contains a color string (or possibly invalid input)
		if pinNum not in validColors:
			print("Invalid entry")
			pinNum = 'red' # default back to valid entry

	if action == 'on' or action == 'off':
		on_off(pinNum,action)

	if action == 'seq':
		seq()

	if action == 'rev_seq':
		rev_seq()

	if action == 'all_on':
		all('on')

	if action == 'all_off':
		all('off')

	if action == 'find_colors':
		find_colors(pinNum)

	if action == 'rand_flash':
		# here pinNum is duration of flash, not GPIO pin#
		rand_flash(pinNum)


	p ={} # new dictionary
	for i in pins:
		p['P' + str(i)] = GPIO.input(i)
	return render_template('index.html', pinStatus=p, pins=pins, colors=colors)

# Pin control functions

# switch on or off individual pins
def on_off(pinNum,action):
	# first verify pinNum is valid
	if pinNum in pins:
		if action == 'on':
			GPIO.output(pinNum, GPIO.HIGH)
		if action == 'off':
			GPIO.output(pinNum, GPIO.LOW)
	else: # pinNum is invalid
		print("Invalid pinNum")
		return

# all ON or OFF
def all(x):
	if x == 'on':
		for i in pins:
			GPIO.output(i, GPIO.HIGH)
	elif x == 'off':
		for i in pins:
			GPIO.output(i, GPIO.LOW)
	else:
		#bad input - do nothing
		return

# flash in sequence, then turn off
def seq():
	for i in pins:
		GPIO.output(i, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(i, GPIO.LOW)
		time.sleep(0.1)
# reverse sequence
def rev_seq():
    for i in reversed(pins):
        GPIO.output(i, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(i, GPIO.LOW)
        time.sleep(0.1)

# Turn on specific colors - Note: x must exist in colors list
def find_colors(color):
	new = []
	for item in range(len(colors)):
		if colors[item] == color:
			new.append(pins[item])
			#return_text(color + ' pins: ' + str(new))
			for i in new:
				GPIO.output(i, GPIO.HIGH)

# flash random pins 'x' times
def rand_flash(x):
	# minor check in case x is too high
	if x > 50:
		x = 50 # just reset to our own limit
	#first turn off all pins
	for i in pins:
		GPIO.output(i, GPIO.LOW)
		time.sleep(0.1)
	for i in range(x):
		pin =  random.choice(pins)
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(0.3)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(0.3)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
