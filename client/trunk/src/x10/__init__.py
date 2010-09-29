"""
General pieces for controlling X10 components.
"""

def enum(*sequential, **named):
	"""Python sucks for not having an enum"""
	enums = dict(zip(sequential, sequential, **named))
	return type('Enum', (), enums)
	
Cmd = enum([
	"ALL_UNITS_OFF",
	"ALL_LIGHTS_ON",
	"ON",
	"OFF"	
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
	"STATUS_REQUEST"])

class Controller(object):
	"""Base class for all X10 controllers, defines the pattern that must be overriden"""

	def send(self, command, house, unit):
		"""Get the code that this controller understands for this type of command"""
		pass
	
	
