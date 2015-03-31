import logging
import ow
import util, x10, config
import x10.powerlinc

# We must init the onewire system
ow.init(config.OWSERVER)

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
Direction = util.enum("UP", "DOWN", "OFF")

#
class Controller(object):
	#
	def __init__(self):
		self.powerlinc = None

	#
	def get_powerlinc(self):
		if not self.powerlinc:
			self.powerlinc = src.x10.powerlinc.PowerLincSerial(config.X10_TTY)

		return self.powerlinc

	#
	def humidify(self, dir):
		"""Make humidity go up/down/off"""
		logging.debug("Change humidity: " + str(dir))
		if dir == Direction.UP:
			self.get_powerlinc().send(x10.Cmd.ON, config.X10_CODE_HUMIDIFIER)
		elif dir == Direction.DOWN:
			self.get_powerlinc().send(x10.Cmd.OFF, config.X10_CODE_HUMIDIFIER)
			logging.error("Don't have a dehumidifier!")
		else:
			self.get_powerlinc().send(x10.Cmd.OFF, config.X10_CODE_HUMIDIFIER)

	#
	def heat(self, dir):
		"""Make temperature go up/down/off"""
		logging.debug("Change temperature: " + str(dir))
		if dir == Direction.UP:
			self.get_powerlinc().send(x10.Cmd.OFF, config.X10_CODE_REFRIGERATOR)
			logging.error("Don't have a heater!")
		elif dir == Direction.DOWN:
			self.get_powerlinc().send(x10.Cmd.ON, config.X10_CODE_REFRIGERATOR)
		else:
			self.get_powerlinc().send(x10.Cmd.OFF, config.X10_CODE_REFRIGERATOR)

	#
	def seek_goals(self, temp, humidity, temp_target, humidity_target):
		"""
		Actually do something about it.
		For the moment this will be a very dumb system.
		"""
		if temp + config.TEMP_MARGIN > temp_target:
			self.heat(Direction.DOWN)
		elif temp - config.TEMP_MARGIN < temp_target:
			self.heat(Direction.UP)
		else:
			self.heat(Direction.OFF)

		if humidity + config.HUMIDITY_MARGIN > humidity_target:
			self.humidify(Direction.DOWN)
		elif humidity - config.HUMIDITY_MARGIN < humidity_target:
			self.humidify(Direction.UP)
		else:
			self.humidify(Direction.OFF)

