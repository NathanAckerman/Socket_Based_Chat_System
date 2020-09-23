import sys
import socket
from _thread import *
import threading 
import time

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
    print("fetching older messages")
    while True:
        msg = s.recv(1024).decode()
        #print(f"message: {msg}\n\n\n")
        msgs = None
        split_text = None
        if "break1234567890" in msg:
            split_text = msg.split("break1234567")
            if len(split_text) > 1:
                msgs = split_text[0].split("msg_break789")
                for msg in msgs:
                    print(msg)
            print("Up to date with messages")
            break
        else: 
            msgs = msg.split("msg_break789")
            for msg in msgs:
                print(msg)


    #not that we have old messages, we will spawn a listening thread for new messages
    #and loop to allow input of messages
    print("type a message and hit enter to send... type quit to quit")
    start_new_thread(thread_func, (s,))
    try:
        #take input from user and send to server
        while True:
            the_input = None
            try:
                the_input = input()
            except EOFError:
                print("Quitting")
                sys.exit()
            if the_input == "quit":
                print("Quitting Client Program")
                sys.exit()
            if the_input == "wait":
                print("waiting")
                while True:
                    time.sleep(.5)
            msg_to_send = the_input.encode('ascii')
            s.send(msg_to_send)
    except (KeyboardInterrupt, SystemExit):
        try:
            s.close()
            sys.exit()
        except:
            sys.exit()
    return


#this function will listen for new messages from the server while the client is online
def thread_func(conn):
    try:
        while True:
            try:
                msg = conn.recv(1024).decode()
                if not msg:
                    conn.close()
                    print("Connection to server is over.")
                    sys.exit(0)
                else:
                    print(msg)
            except:
                conn.close()
                sys.exit()
    except (KeyboardInterrupt, SystemExit):
        try:
            conn.close()
            sys.exit()
        except:
            sys.exit()


if __name__ == "__main__":
    main()
