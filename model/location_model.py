import csv
import uuid
import pymongo
import geopy.distance

client = pymongo.MongoClient(
	"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
db_posts = client.test_database.posts

class LocationModel:
	@staticmethod
	def get_pin(args): # args: _id (pin id)
		# returns the park name, lat and long of pin
		dummy_pin = args["_id"]
		pin = db_posts.find({"_id": dummy_pin}).next()
		return pin.get("park"), pin.get("latitude"), pin.get("longitude")

	@staticmethod
	def get_pins(args):
		# returns the names and coordinates of landmarks within 25 km of user
		# return format tuple: (name, (latitude, longitude))
		name = ""
		max_dist = 100 # km
		within_max_dist_lst = []
		user_coords   = (args["latitude"], args["longitude"])
		custom_coords = db_posts.find({"park": args["parkId"], "custom": True}) # grabs all user-created landmarks in park
		for loc in custom_coords:
			loc_coords = (loc.get("latitude"), loc.get("longitude"))
			dist = geopy.distance.distance(user_coords, loc_coords).km
			if dist < max_dist:
				within_max_dist_lst.append(loc_coords)
		return {"pins": within_max_dist_lst}

	@staticmethod
	def get_closest_park(args): # args: latitude, longitude, radius
		# gets the closest park in order to determine which pins to get
		latitude  = args["latitude"]
		longitude = args["longitude"]
		radius    = args["radius"]

		parks = []
		dists = []
		pparks = db_posts.find({"custom": False})

		for ppark in pparks:
			ppark_coords = (ppark.get("latitude"), ppark.get("longitude"))
			dist = geopy.distance.distance((latitude, longitude), ppark_coords)
			if dist <= radius:
				parks.append(ppark.get("_id"))
				dists.append(dist)

		if len(parks) == 1:
			return parks[0]
		elif len(parks) > 1:
			return parks[dists.index(min(dists))]
		else:
			args["radius"] += 50
			return LocationModel.get_closest_park(args)

	@staticmethod
	def populate(): # should only be called once
		# populates the db with national parks
		with open("nat_parks.csv") as file:
			reader = csv.reader(file, delimiter = ",")
			for row in reader:
				if (row[0] == "Name"):
					continue
				post = {"_id": row[0],
						"latitude": row[1],
						"longitude": row[2],
						"custom": False,
				}
				db_posts.insert_one(post)

	@staticmethod
	def add_pin(args): # args: park, latitude, longitude

		# user_id references the "_id" from the User class
		# users can add a pin (press + hold) to a national park to increase awareness
		# hopefully can add a photo in the future
		park      = args["park"]
		latitude  = args["latitude"]
		longitude = args["longitude"]

		ppark = db_posts.find({"_id": park, "custom": False}).next()
		ppark_coords = (ppark.get("latitude"), ppark.get("longitude"))
		if geopy.distance.distance(ppark_coords, (latitude, longitude)).km < 550:
			post = {"_id": uuid.uuid4(),
					"park": park,
					"latitude": latitude,
					"longitude": longitude,
					"custom": True,
			}
			db_posts.insert_one(post)
		else:
			print("Sorry, too far from an endpoint to post.")



