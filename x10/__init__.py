"""
General stuff for controlling X10 components. This code has just been shoved here; it once
worked but it probably won't without some massaging.
"""
import util
from x10 import powerlinc
import config
import logging

Cmd = util.enum(
	"ALL_UNITS_OFF",
	"ALL_LIGHTS_ON",
	"ON",
	"OFF",
	"DIM",
	"BRIGHT",
	"ALL_LIGHTS_OFF",
	"EXTENDED_CODE",
	"HAIL_REQUEST",
	"PRESET_DIM_HIGH",
	"PRESET_DIM_LOW",
	"EXTENDED_DATA",
	"STATUS_ON",
	"STATUS_OFF",
	"STATUS_REQUEST")


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
			self.powerlinc = powerlinc.PowerLincSerial(config.X10_TTY)

		return self.powerlinc

	#
	def humidify(self, dir):
		"""Make humidity go up/down/off"""
		logging.debug("Change humidity: " + str(dir))
		if dir == Direction.UP:
			self.get_powerlinc().send(Cmd.ON, config.X10_CODE_HUMIDIFIER)
		elif dir == Direction.DOWN:
			self.get_powerlinc().send(Cmd.OFF, config.X10_CODE_HUMIDIFIER)
			logging.error("Don't have a dehumidifier!")
		else:
			self.get_powerlinc().send(Cmd.OFF, config.X10_CODE_HUMIDIFIER)

	#
	def heat(self, dir):
		"""Make temperature go up/down/off"""
		logging.debug("Change temperature: " + str(dir))
		if dir == Direction.UP:
			self.get_powerlinc().send(Cmd.OFF, config.X10_CODE_REFRIGERATOR)
			logging.error("Don't have a heater!")
		elif dir == Direction.DOWN:
			self.get_powerlinc().send(Cmd.ON, config.X10_CODE_REFRIGERATOR)
		else:
			self.get_powerlinc().send(Cmd.OFF, config.X10_CODE_REFRIGERATOR)

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

