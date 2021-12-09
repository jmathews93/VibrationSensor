from coapthon.server.coap import CoAP
from exampleresources import BasicResource
import argparse

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('basic/', BasicResource())

def main(args):
    server = CoAPServer("0.0.0.0", args['port'])
    try:
        print("Listening on Port", args['port'], "...")
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = vars(parser.parse_args())
    print(args)
    main(args)
