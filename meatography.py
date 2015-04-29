#!/usr/bin/python
#
# Despite what http://nicomiceli.com/tracking-your-home-with-google-analytics/ says, Google Analytics
# sucks for this kind of data. So abandoning that, we made our own backend that guns on Google App Engine.
#
# This script should be run from cron once per minute.

import urllib2
import logging
import hardware
import config
import json

# Log if you want it
logging.getLogger().setLevel(logging.DEBUG)

# Get the real values
tempC = hardware.get_temp()
humidity = hardware.get_humidity()

logging.info(u"{0}\u00b0C, {1}% humidity".format(tempC, humidity))

# Make the call to the server
measurement = {
	"t": tempC,
	"h": humidity
}

req = urllib2.Request(config.SUBMIT)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(measurement))

#logging.info(config.SUBMIT + " responded with " + response.read())

