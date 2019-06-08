from math import sin, cos, sqrt, atan2, radians

pins = set() # temp in lieu of the db, should be in backend

class Location:

	radius = 6373.0 # km (radius of earth)

	def __init__(name, latitude, longitude):
		self.name = name
		self.lat  = radians(latitude)
		self.long = radians(longitude)

	def closest_location(self, loc_set): # loc_set refers to pins
		# returns the Location object closest to self
		# returns the min_dist
		name = ""
		closest_loc = None # Location object to be returned
		min_dist = 50

		for loc in loc_set:
			dlat  = loc.lat  - self.lat
			dlong = loc.long - self.long

			a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			dist = radius * c

			if dist < min_dist:
				closest_loc = loc
				min_dist = dist

		return name, closest_loc, min_dist

	def add_pin(location):
		pins.add(location)
		# send to db


