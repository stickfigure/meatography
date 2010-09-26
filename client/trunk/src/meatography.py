#
# Script which controlls a meatography cabinet, submitting temperature and humidity values
# to a server and actuating control devices to maintain stable values.
#
# This script should be run from cron once per minute.
#
# It reads a config file called meatography.cfg which is expected to look like this:
#
# [meatography]
# cabinet_id=nameOfYourCabinet	# name of your cabinet in the server
# owserver=localhost:4304	# how to access the onewire server; could be "u" for usb directly
# server_url=http://www.meatography.com/submit	# url of the server

import urllib
import urllib2
import logging
import datetime
import time
import ow
import ConfigParser

# The defaults - change your local settings in a meatography.cfg file
cfg_filename = "meatography.cfg"
cfg_section = "meatography"
cfg_owserver_param = "owserver"
cfg_server_url_param = "server_url"
cfg_cabinet_id_param = "cabinet_id"
cfg_defaults = {
			cfg_owserver_param: "localhost:4304",
			cfg_server_url_param: "http://www.meatography.com/submit"
			}

# Log if you want it
logging.getLogger().setLevel(logging.DEBUG)

#
def get_temp_sensor():
	#return ow.Sensor("/10.FF09E6010800")
	tempSensors = ow.Sensor("/").find(family="10")
	if not tempSensors:
		raise Exception, "Unable to find temperature sensor"
	elif len(tempSensors) > 1:
		raise Exception, "Too many temperature sensors on bus"
	else:
		return tempSensors[0]

#
def get_humidity_sensor():
	#return ow.Sensor("/26.C9C9F1000000")
	humiditySensors = ow.Sensor("/").find(family="26")
	if not humiditySensors:
		raise Exception, "Unable to find humidity sensor"
	elif len(humiditySensors) > 1:
		raise Exception, "Too many humidity sensors on bus"
	else:
		return humiditySensors[0]

	
#
# Let the program continue
#
cfg = ConfigParser.ConfigParser(cfg_defaults)
cfg.read(cfg_filename)
ow.init(cfg.get(cfg_section, cfg_owserver_param))
tempSensor = get_temp_sensor()
humiditySensor = get_humidity_sensor()

# Get the real values
temp = float(tempSensor.temperature)
humidity = float(humiditySensor.humidity)

logging.info(u"Temperature is {0}\u00b0C".format(temp))
logging.info(u"Humidity is {0}%".format(humidity))

# Make the call to the server
params = {}
params["ver"] = 1
params["cid"] = cfg.get(cfg_section, cfg_cabinet_id_param)
params["when"] = time.mktime(datetime.datetime.now().timetuple()) * 1000	# java time format
params["temp"] = temp
params["humidity"] = humidity

encoded_params = urllib.urlencode(params)

response = urllib2.urlopen(cfg.get(cfg_section, cfg_server_url_param), encoded_params)