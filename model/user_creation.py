import pymongo

class User:

	client = pymongo.MongoClient(
		"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
	db_posts = client.test_database.posts

	@staticmethod
	def register(username, email, password):
		db_posts.insert_one({"username": username,
			"email": email,
			"password": password,
			})

	@staticmethod
	def login(username, password):
		return db_posts.find({"username": username, "password": password}).hasNext()