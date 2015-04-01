import ow
import config

# We must init the onewire system
ow.init(config.OWSERVER)

#
def get_temp():
	def get_temp_sensor():
		tempSensors = list(ow.Sensor("/").find(family="10"))
		if not tempSensors:
			raise Exception, "Unable to find temperature sensor"
		elif len(tempSensors) > 1:
			raise Exception, "Too many temperature sensors on bus"
		else:
			return tempSensors[0]

	return float(get_temp_sensor().temperature)

#
def get_humidity():
	def get_humidity_sensor():
		#return ow.Sensor("/26.C9C9F1000000")
		humiditySensors = list(ow.Sensor("/").find(family="26"))
		if not humiditySensors:
			raise Exception, "Unable to find humidity sensor"
		elif len(humiditySensors) > 1:
			raise Exception, "Too many humidity sensors on bus"
		else:
			return humiditySensors[0]

	return float(get_humidity_sensor().humidity)

