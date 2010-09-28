#!/usr/bin/python
#
# Script which controlls a meatography cabinet, submitting temperature and humidity values
# to a server and actuating control devices to maintain stable values.
#
# This script should be run from cron once per minute.
#
# The first parameter is expected to be a config file which is expected to look like this:
#
# [meatography]
# cabinet_id=nameOfYourCabinet	# name of your cabinet in the server
# owserver=localhost:4304	# how to access the onewire server; could be "u" for usb directly
# server_url=http://www.meatography.com/submit	# url of the server
#
# More config values can be found in the config.py file.

import urllib
import urllib2
import logging
import datetime
import time
import json
import hardware
import config

# Log if you want it
logging.getLogger().setLevel(logging.DEBUG)

# Get the real values
temp = hardware.get_temp()
humidity = hardware.get_humidity()

logging.info(u"{0}\u00b0C, {1}% humidity".format(temp, humidity))

# Make the call to the server
params = {}
params["ver"] = 1
params["cid"] = config.CABINET_ID
params["when"] = time.mktime(datetime.datetime.now().timetuple()) * 1000	# java time format
params["temp"] = temp
params["humidity"] = humidity

encoded_params = urllib.urlencode(params)

raw_response = urllib2.urlopen(config.SERVER_URL, encoded_params)
response = json.load(raw_response)

temp_target = float(response['tempTarget'])
humidity_target = float(response['humidityTarget'])

hardware.seek_goals(temp, humidity, temp_target, humidity_target)


