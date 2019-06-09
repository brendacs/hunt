import pymongo

client = pymongo.MongoClient(
	"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
db_posts = client.test_database.posts

class User:
	@staticmethod
	def register(args):
		db_posts.insert_one({"_id": args["username"],
			"email": args["email"],
			"password": args["password"],
			})

	@staticmethod
	def login(args):
		try:
			user = db_posts.find({"_id": args["username"]})
			return user.next()
		except:
			return {"error": "Invalid credentials.", "code": 401}
