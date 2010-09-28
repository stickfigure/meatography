import ow
import config
import logging

#
def get_temp():
	def get_temp_sensor():
		#return ow.Sensor("/10.FF09E6010800")
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

#
def is_cooler_on():
	"""Return the current status of the cooler device"""
	return False

#
def is_heater_on():
	"""Return the current status of the heater device"""
	return False

#
def is_humidifier_on():
	"""Return the current status of the humidifier device"""
	return False

#
def is_dehumidifier_on():
	"""Return the current status of the dehumidifier device"""
	return False

#
def humidify(on):
	"""Switch the humidifier on or off"""
	logging.debug("Humidifier: " + str(on))

#
def dehumidify(on):
	"""Switch the dehumidifier on or off"""
	logging.debug("Dehumidifier: " + str(on))
	
#
def cool(on):
	"""Switch the cooler on or off"""
	logging.debug("Cooler: " + str(on))
	
#
def heat(on):
	"""Switch the heater on or off"""
	logging.debug("Heater: " + str(on))
	
#
def seek_goals(temp, humidity, temp_target, humidity_target):
	"""
	Actually do something about it.
	For the moment this will be a very dumb system.
	"""
	if temp + config.TEMP_MARGIN > temp_target:
		heat(False)
		cool(True)
	elif temp - config.TEMP_MARGIN < temp_target:
		heat(True)
		cool(False)
	else:
		heat(False)
		cool(False)
		
	if humidity + config.HUMIDITY_MARGIN > humidity_target:
		humidify(False)
		dehumidify(True)
	elif humidity - config.HUMIDITY_MARGIN < humidity_target:
		humidify(True)
		dehumidify(False)
	else:
		humidify(False)
		dehumidify(False)
	
# We must init the onewire system
ow.init(config.OWSERVER)
