import pymongo
import geopy.distance


client = pymongo.MongoClient(
	"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
db = client.test_database

#use [database];
#db.dropDatabase();

class Location:

	radius = 6373.0 # km (radius of earth)

	def __init__(name, latitude, longitude):
		self.name      = name
		self.latitude  = latitude
		self.longitude = longitude

	def closest_location(self, park):
		# returns the name of landmark closest to user
		# returns the distance from user
		name = ""
		min_dist = 50 # km

		cursor = db.posts.find({"park": park}) # grabs all landmarks in park

		user_coords = (self.latitude, self.longitude)

		for loc in cursor:
			loc_coords = (loc.latitude, loc.longitude)

			dist = geopy.distance.vincenty(user_coords, loc_coords).km

			if dist < min_dist:
				dist = min_dist
				name = loc.name

		return name, min_dist

	def add_pin(park, name, latitude, longitude):
		post = {"park": park,
				"name": name,
				"latitude": latitude,
				"longitude": longitude,
		}
		db.posts.insert_one(post)
		# send to db


