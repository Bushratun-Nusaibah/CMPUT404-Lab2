#!/usr/bin/env python3
from multiprocessing.dummy import Process
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        #AF_INET = IpV4
        #SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def echo_handler(proxy_end, conn, address):
    #recieve data, wait a bit, then send it back
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending recieved data {send_full_data} to google")
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending recieved data {data} to google")
    time.sleep(0.5)
    conn.sendall(data)


def main():

    google_host = 'www.google.com'
    google_port = 80

    #requests a page from google
    buffer_size = 4096
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
            
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
                
            #create a new socket 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
                remote_ip = get_remote_ip(google_host)
                proxy_socket.connect((remote_ip , google_port))
                print (f'Socket Connected to {google_host} on ip {remote_ip}')
                #recieve data, wait a bit, then send it back
                    
                p = Process(target=echo_handler, args=(proxy_socket, conn, addr))
                p.daemon = True
                p.start()
                print("Started Process", p)

            conn.close()
   

if __name__ == "__main__":
    main()
