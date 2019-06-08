import hashlib

class Login:

	def __init__(username, password):
		hash_id = hash256(username, password)
		# check if hash_id exists in db


class Register:
	def __init__(username, name, password):
		# check if username is available
		hash_id = hash256(username, password)
		#put into db



		

	@staticmethod
	def hash256(value1, value2):
		h = hashlib.sha256()
		value1 = value1.lower().encode("utf-8")
		value2 = value2.lower().encode("utf-8")
		h.update(value1)
		h.update(value2)
		return h.hexdigest()