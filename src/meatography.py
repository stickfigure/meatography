#!/usr/bin/python
#
# For the moment this just reports data to Google Analytics
#
# This script should be run from cron once per minute.

# import urllib
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

# Send it to GA
url1 = "http://www.google-analytics.com/collect?v=1&tid={0}&cid=1&t=event&ec=Environment&ea=temperature&el=${1}&ev={2}".format(config.GAID, config.LABEL, gaTempF)
urllib2.urlopen(url1).close

url2 = "http://www.google-analytics.com/collect?v=1&tid={0}&cid=1&t=event&ec=Environment&ea=humidity&el=${1}&ev={2}".format(config.GAID, config.LABEL, gaHumidity)
urllib2.urlopen(url2).close
