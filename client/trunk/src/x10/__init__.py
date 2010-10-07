"""
General stuff for controlling X10 components.
"""
import util

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
