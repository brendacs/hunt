import pymongo
client = pymongo.MongoClient(
	"mongodb+srv://admin:adminadmin@cluster0-dhc2n.mongodb.net/test?retryWrites=true&w=majority")
db_posts = client.test_database.posts

#db_posts.insert_one({
#	"_id": "primal",
#	"username":"yooy"
#	})

db_posts.insert_one({
	"_id": "crimal",
	"username":"yooy"
	})


user = db_posts.find({"username": "yooy"})

for u in user:



	print(u)