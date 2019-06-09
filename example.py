from model.location_model import LocationModel
import random as rand

# "Yosemite"
# lat: "37.83"
# long: "-119.5"
# custom: false

def setup(num_pin = 50):
	pin_num = 0

	while (pin_num < num_pin):
		lat_rand  = rand.uniform(-0.75, 0.75)
		long_rand = rand.uniform(-0.75, 0.75)
		arg       = {"park": "Yosemite", "latitude": 37.83 + lat_rand, "longitude": -119.5 + long_rand}
		LocationModel.add_pin(arg)

	pin_num += 1

