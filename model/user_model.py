import pymongo

client = pymongo.MongoClient(
	"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
db_posts = client.test_database.posts

class User:
	@staticmethod
	def register(username, email, password):
		db_posts.insert_one({"_id": username,
			"email": email,
			"password": password,
			})

	@staticmethod
	def login(username, password):
		try:
			user = db_posts.find({"_id": username})
			return user.next()
		except:
			return {"error": "Invalid credentials.", "code": 401}
