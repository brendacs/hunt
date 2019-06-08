from math import sin, cos, sqrt, atan2, radians

class Model:

	def __init__():
		# do inits here


class Location:

	radius = 6373.0 # km (radius of earth)

	def __init__(latitude, longitude):
		self.lat  = radians(latitude)
		self.long = radians(longitude)

	def closest_location(self, loc_set):
		for loc in loc_set:
			dlon = 