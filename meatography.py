#!/usr/bin/python
#
# For the moment this just reports data to Google Analytics
# Based on: http://nicomiceli.com/tracking-your-home-with-google-analytics/
#
# This script should be run from cron once per minute.

import urllib
import urllib2
import logging
import hardware
import config

# Log if you want it
logging.getLogger().setLevel(logging.DEBUG)

# Get the real values
tempC = hardware.get_temp()
tempF = tempC * 1.8 + 32
humidity = hardware.get_humidity()

logging.info(u"{0}\u00b0F, {1}% humidity".format(tempF, humidity))

# need to make them into integers for GA, multiply by 10 to increase precision
gaTempF = max(0, int(round(tempF*10)))
gaHumidity = max(0, int(round(humidity*10)))

def hit_ga(action, value):
    params = {
        "v": "1",
        "tid": config.GAID,
        "cid": "1",
        "t": "event",
        "ec": "Environment",
        "ea": action,
        "el": config.LABEL,
        "ev": value
    }
    data = urllib.urlencode(params)
    req = urllib2.Request("http://www.google-analytics.com/collect", data)
    logging.info("Posting: " + str(req))
    urllib2.urlopen(req).close

hit_ga("temperature", gaTempF)
hit_ga("humidity", gaHumidity)