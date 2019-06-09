import csv
import pymongo
import geopy.distance
from model.model import Model

class Location:

	client = pymongo.MongoClient(
		"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
	db_posts = client.test_database.posts

	@staticmethod
	def get_pins(latitude, longitude, park):
		# returns the names and coordinates of landmarks within 25 km of user
		# return format tuple: (name, (latitude, longitude))
		name = ""
		max_dist = 50 # km
		within_max_dist_lst = []
		user_coords   = (latitude, longitude)
		custom_coords = db_posts.find({"park": park, "custom": True}) # grabs all user-created landmarks in park

		for loc in user_coords:
			loc_coords = (loc.get("latitude"), loc.get("longitude"))
			dist = geopy.distance.distance(user_coords, loc_coords).km
			if dist < max_dist:
				within_max_dist_lst.append((loc.get("name"), loc_coords))
		return within_max_dist_lst

	def get_closest_park(latitude, longitude, radius = 50):
		if radius >= 550:
			return None

		parks = []
		dists = []
		pparks = db_posts.find({"custom": False})
		for ppark in pparks:
			ppark_coords = (ppark.get("latitude"), ppark.get("longitude"))
			dist = geopy.distance.distance((latitude, longitude), ppark_coords)
			if dist <= radius:
				parks.append(ppark.get("park"))
				dists.append(dist)

		if len(parks) == 1:
			return parks[0]
		elif len(parks) > 1:
			return parks[dists.index(min(dists))]
		else:
			return get_closest_park(latitude, longitude, radius + 50)

	@staticmethod
	def populate(): # should only be called once
		# populates the db with national parks
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
				db_posts.insert_one(post)

	def add_pin(park, latitude, longitude): # user created pins
		ppark = db_posts.findOne({"park": park, "custom": False})
		ppark_coords = (ppark.get("latitude"), ppark.get("longitude"))
		if geopy.distance.distance(ppark_coords, (latitude, longitude)).km < 550:
			post = {"park": park,
					"latitude": latitude,
					"longitude": longitude,
					"custom": True,
			}
			db_posts.insert_one(post)
		else:
			print("Sorry, too far from an endpoint to post.")

