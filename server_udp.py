import socket


def main(args):
    
    localIP = "0.0.0.0"
    localPort = args['port']
    bufferSize = 1024

    msgFromServer = "Hello UDP Client"
    bytesToSend = str.encode(msgFromServer)


    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")
    
    f = open('data.csv', "a")

    # Listen for incoming datagrams
    while(True):
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP  = "Client IP Address:{}".format(address)

            print(clientMsg)
            print(clientIP)
        
            # Write to File
            f.write(message)
        except KeyboardInterrupt:
            break
    f.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ipaddress", type=str, default='0.0.0.0')
    parser.add_argument("-f", "--filename", type=str, default='data.csv')
    parser.add_argument("-p", "--port", type=str, default=8080)
    args = vars(parser.parse_args())
    print(args)
    main(args)
