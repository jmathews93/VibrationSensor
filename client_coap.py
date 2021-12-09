from coapthon.client.helperclient import HelperClient
import json, sys
import argparse
from time import sleep

# Hard limit of 9203 for the substring/ character limit

def test_case_1(data, client, loop_len, path):
    # global data, client, loop_len
    """
    Sends each record in the JSON file separately.
    """

    for i in range(600):
        list = []
        list.append(data['allTides'][i]['time'])
        list.append(data['allTides'][i]['height'])
        client.put(path, str(list))


def test_case_2(client, jsn, path):
    # global client, jsn
    """
    Sends the first 9203 characters (bytes) in the string representation
    of the json file.
    """

    for i in range(300):
        client.put(path, jsn[0:9203])


def test_case_3(client, jsn, path):
    # global jsn
    """
    Sends the first 65000 characters in the string representation
    of the json file to simulate a max packet size.
    """

    for i in range(100):
        client.put(path, jsn[0:65000])


def main(args):
    file = open(args['filename'], "r")
    jsn = file.read()

    with open(args['filename']) as f:
        data = json.load(f)

    loop_len = len(data['allTides'])    

    host = args['ipaddress']
    port = int(args['port'])
    path = "basic"

    client = HelperClient(server=(host, port))

    client.put(path, str(1))
    sleep(1)

    if args['test'] == "1":
        print "Test Case 1:"
        for i in range(10):
            print "Trial", i, "\n"
            test_case_1(data, client, loop_len, path)
            print "End Trial", i, "\n"
            sleep(0.2)
    elif args['test'] == "2":
        print "Test Case 2:"
        for i in range(10):
            print "Trial", i, ":"
            test_case_2(client, jsn, path)
            print "End Trial", i, "\n"
            sleep(0.2)
        sleep(15)
    else:
        print "Test Case 3"
        for i in range(10):
            print "Trial", i, ":"
            test_case_3(client, jsn, path)
            print "End Trial", i, "\n"
            sleep(0.2)

    client.put(path, str(1))
    client.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ipaddress", type=str, required=True)
    parser.add_argument("-f", "--filename", type=str, required=True)
    parser.add_argument("-t", "--test", choices=["1", "2", "3"], default="1")
    parser.add_argument("-p", "--port", type=str, default=8080)
    args = vars(parser.parse_args())
    print(args)
    main(args)
