"""
General utilities
"""

def enum(*sequential, **named):
	"""Python sucks for not having an enum"""
	enums = dict(zip(sequential, sequential), **named)
	return type('Enum', (), enums)
