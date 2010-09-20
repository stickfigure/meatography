import urllib2
import logging
from datetime import datetime
import time
import ow

config = {}

# Configure this with a unique id for the cabinet
config["cabinet_id"] = "cabinet0"
#config["owserver"] = "u"	# for direct USB access, don't run the server

# Access to the onewire server
config["owserver"] = "localhost:4304"

# Base url to the server
config["server_url"] = "http://www.meatography.com/submit"

# Log if you want it
logging.getLogger().setLevel(logging.DEBUG)

#
# Let the program continue
#
ow.init(config["owserver"])
sensTemp = ow.Sensor("/10.FF09E6010800")
sensHumid = ow.Sensor("/26.C9C9F1000000")

temp = float(sensTemp.temperature)
humidity = float(sensHumid.humidity)

logging.info(u"Temp is {0}\u00b0C".format(temp))
logging.info(u"Humidity is {0}%".format(humidity))

params = {}
params["ver"] = 1
params["cid"] = config["cabinet_id"]
params["when"] = time.mktime(datetime.now().timetuple()) * 1000	# java time format
