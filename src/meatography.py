#!/usr/bin/python
#
# Script which controlls a meatography cabinet, submitting temperature and humidity values
# to a server and actuating control devices to maintain stable values.
#
# This script should be run from cron once per minute.

# import urllib
# import urllib2
import logging
# import datetime
# import time
# import json
import hardware

# Log if you want it
logging.getLogger().setLevel(logging.DEBUG)

# Get the real values
temp = hardware.get_temp()
humidity = hardware.get_humidity()

logging.info(u"{0}\u00b0C, {1}% humidity".format(temp, humidity))

# Make the call to the server
# params = {}
# params["ver"] = 1
# params["cid"] = config.CABINET_ID
# params["when"] = int(time.mktime(datetime.datetime.now().timetuple()))
# params["temp"] = temp
# params["humidity"] = humidity

# encoded_params = urllib.urlencode(params)

#logging.info(encoded_params)

# raw_response = urllib2.urlopen(config.SERVER_URL, encoded_params)
# response = json.load(raw_response)
#
# temp_target = float(response['tempTarget'])
# humidity_target = float(response['humidityTarget'])

#ctl = hardware.Controller()
#ctl.seek_goals(temp, humidity, temp_target, humidity_target)


