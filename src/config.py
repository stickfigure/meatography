import sys
import ConfigParser


# The defaults - change your local settings in a meatography.cfg file
sect = "meatography"
cfg_defaults = {
			"owserver": "localhost:4304",
			"server_url": "http://www.meatography.com/meat/submit",
			"temp_margin": "2",
			"humidity_margin": "2",
			"x10_tty": "/dev/ttyUSB0",
			"x10_refrigerator": "M1",
			"x10_humidifier": "M2"
			}
cfg = ConfigParser.ConfigParser(cfg_defaults)
cfg.read(sys.argv[1])
	
# Actually use these from code
OWSERVER = cfg.get(sect, "owserver")
SERVER_URL = cfg.get(sect, "server_url")
CABINET_ID = cfg.get(sect, "cabinet_id")
TEMP_MARGIN = cfg.getfloat(sect, "temp_margin")
HUMIDITY_MARGIN = cfg.getfloat(sect, "humidity_margin")

X10_TTY = cfg.get(sect, "x10_tty")
X10_CODE_REFRIGERATOR = cfg.get(sect, "x10_refrigerator")
X10_CODE_HUMIDIFIER = cfg.get(sect, "x10_humidifier")