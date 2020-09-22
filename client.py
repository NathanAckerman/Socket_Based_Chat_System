import sys
import socket
from _thread import *
import threading 

def main():
    client_id_arg = sys.argv[2]
    server_ip_arg = sys.argv[4]
    port_arg = sys.argv[6]

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_ip_arg, int(port_arg)))
    s.send(client_id_arg.encode('ascii'))
    accept_msg = s.recv(1024).decode()
    if accept_msg == "REFUSE":
        print("Connection Refused. Bad Client ID")
        sys.exit()
    #get old messages
    #while True:
     #   msg = s.recv(1024).decode()
      #  if msg == "break":
       #     print("You are up to date on messages")
        #    break
        #else: 
         #   print(msg)
    print("type a message and hit enter to send... type quit to quit")
    start_new_thread(thread_func, (s,))
    try:
        while True:
            the_input = input()
            if the_input == "quit":
                print("Quitting")
                sys.exit()
            msg_to_send = the_input.encode('ascii')
            s.send(msg_to_send)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
    return

def thread_func(conn):
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                conn.close()
                print("Connection to server is over.")
                sys.exit(0)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()


if __name__ == "__main__":
    main()
