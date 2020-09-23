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
    #get old messages from server
    print("fetching older messages")
    while True:
        msg = s.recv(1024).decode()
        msgs = None
        split_text = None
        #this msg means we are up to date
        if "break1234567890" in msg:
            split_text = msg.split("break1234567")
            #if there are other messages bundled with the end msg
            if len(split_text) > 1:
                msgs = split_text[0].split("msg_break789")
                for msg in msgs:
                    print(f"{client_id_arg}'s console: {msg}")
            print("Up to date with messages")
            break
        else: #all msgs are valid msgs and there will be more
            msgs = msg.split("msg_break789")
            for msg in msgs:
                print(f"{client_id_arg}'s console: {msg}")


    #not that we have old messages, we will spawn a listening thread for new messages
    #and loop to allow input of messages
    print("type a message and hit enter to send... type quit to quit")
    start_new_thread(thread_func, (s,client_id_arg,))
    try:
        #take input from user and send to server
        while True:
            the_input = None
            try:#this try/except is needed when reading msgs in from file
                the_input = input()
            except EOFError:
                sys.exit()
            if the_input == "quit":
                print("Quitting Client Program")
                sys.exit()
            if the_input == "wait":
                print("waiting")
                counter = 0
                while counter < 10:
                    time.sleep(.5)
                    counter += 1
                continue
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
def thread_func(conn, client_id):
    try:
        while True:
            try:
                msg = conn.recv(1024).decode()
                if not msg:#if connection is broken
                    conn.close()
                    print("Connection to server is over.")
                    sys.exit(0)
                else:
                    print(f"{client_id}'s console: {msg}")
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
