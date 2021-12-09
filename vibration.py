import RPi.GPIO as GPIO
from coapthon.client.helperclient import HelperClient
import time


def main(args):
	# GPIO SETUP
	channel = 17
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(channel, GPIO.IN)
 
	# Setupo Coap Client
	host = args['ipaddress']
    port = int(args['port'])
    path = "basic"
    client = HelperClient(server=(host, port))
 
	# Open data file for writing inputs
	f = open('data.csv', "a")
	f.write("data, time, deviceNum")

	# Continuously read vibration info until CTRL-C
	while True:
		try:
			input_value = GPIO.input(channel)
			print(input_value, time.time())
			data_point = "{},{},{}\n".format(input_value, time.time(), args["deviceNum"])
			f.write(data_point)
   			client.post(path, rand_word(random.randint(100, 300)))
		except KeyboardInterrupt:
			break
	f.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ipaddress", type=str, required=True)
    parser.add_argument("-f", "--filename", type=str)
    parser.add_argument("-p", "--port", type=str, default=8080)
    parser.add_argument("-dn", "--deviceNum", type=int, default=1)
    args = vars(parser.parse_args())
    print(args)
    main(args)
