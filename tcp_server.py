import socket
import threading

def on_new_client(connection, f):
    while(True):
        try:
            # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            data = connection.recv(16)
                
            if data:
                clientMsg = "Message from Client:{}".format(data)
                        
                print("Data: {}".format(data.decode("utf-8")))
                        
                # Write to File
                f.write(data.decode("utf-8"))
                        
            else:
                break
        except KeyboardInterrupt:
            connection.close()
            break
    f.close()

def main(args):
    
    localIP = "0.0.0.0"
    localPort = args['port']
    bufferSize = 2048



    # Create a datagram socket
    # UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("Setting up Server...\n")
    TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    

    # Bind to address and ip
    # UDPServerSocket.bind((localIP, localPort))
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((localIP, localPort))
    
    print("Listening for connection...\n")
    TCPServerSocket.listen(1)

    print("UDP server up and listening")
    
    f = open('data.csv', "a")

    # Listen for incoming datagrams
    threads = []
    
    while(True):
        try:
            connection, client_address = TCPServerSocket.accept()
            x = threading.Thread(target=on_new_client, args=(connection,f))
            threads.append(x)
            x.start()
        except KeyboardInterrupt:
            # Clean up the connection
            print("Shutting Server Down")
            connection.close()
            
            for i in threads:
                i.join()
            break
            


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ipaddress", type=str, default='0.0.0.0')
    parser.add_argument("-f", "--filename", type=str, default='data.csv')
    parser.add_argument("-p", "--port", type=str, default=8080)
    args = vars(parser.parse_args())
    print(args)
    main(args)
