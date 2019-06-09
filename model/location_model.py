import csv
import pymongo
import geopy.distance
from model.model import Model


client = pymongo.MongoClient(
	"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
db = client.test_database

class LocationModel(Model):
	function_arguments = {
		"get_pins": {
			"latitude": str,
			"longitude": float
		},
		"add_pin": {
			"parkId": str,
			"name": str,
			"latitude": float,
			"longitude": float
		}
	}

# TODO: Add pin_info api

	@staticmethod
	def get_pins(request):
		# returns the names and coordinates of landmarks within 25 km of user
		# return format tuple: (name, (latitude, longitude))
		name = ""
		max_dist = 25 # km

		cursor = db.posts.find({"park": park}) # grabs all landmarks in park

		user_coords = (latitude, longitude)

		within_max_dist_lst = []

		for loc in cursor:
			loc_coords = (loc.get("latitude"), loc.get("longitude"))

			dist = geopy.distance.distance(user_coords, loc_coords).km

			if dist < max_dist:
				within_max_dist_lst.append((loc.get("name"), loc_coords))

		return within_max_dist_lst

	def closest_park(latitude, logitude):
		# do this wesley

	def populate(): # should only be called once
		with open("nat_parks.csv") as file:
			reader = csv.reader(file, delimiter = ",")
			for row in reader:
				if (row[0].equals("Name")):
					continue
				post = {"park": row[0],
						"latitude": row[1],
						"longitude": row[2],
						"custom": False,
				}
				db.posts.insert_one(post)



	def add_pin(park, name, latitude, longitude):
		post = {"park": park,
				"latitude": latitude,
				"longitude": longitude,
				"custom": True,
		}
		db.posts.insert_one(post)
		# send to db
