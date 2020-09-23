import sys
import socket
from _thread import *
import threading 


#since python doesnt have struct and i need to C
#these are variables used by all of the threads to coordinate messages
#any access to these must be guarded by a lock
class GlobalVars():
    all_client_ids = None
    next_msg_id = 0
    global_lock = threading.Lock()
    all_msgs = []
    all_users = []

def main():
    clients_arg = sys.argv[2]
    port_arg = sys.argv[4]
    clients_list = clients_arg.split(",")
    GlobalVars.all_client_ids = clients_list
    print(f"Starting server on port {port_arg} with clients {clients_list}")

    #set up socket to listen on
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", int(port_arg)))
    sock.listen(len(clients_list)+5)
    try:
        #infinite loop to accept connections
        while True:
            conn, addr = sock.accept()
            #spawn new thread to deal with connection
            start_new_thread(thread_func, (conn,))
    
    except (KeyboardInterrupt, SystemExit):
        print("exiting. closing connections.")
        cleanup_connections()
        sys.exit()
    return

#on exit, clean the connections
def cleanup_connections():
    for user in GlobalVars.all_users:
        if user.isConnected:
            try:
                user.connection.close()
            except:
                pass

#this thread handles the actual connection to a client
def thread_func(conn): 
    #first msg is always the client id
    client_id = conn.recv(1024).decode()
    #if the id is not one of the approved ids
    if client_id not in GlobalVars.all_client_ids:
        GlobalVars.global_lock.acquire()
        print(f"Refusing connection with client {client_id}")
        GlobalVars.global_lock.release()
        ref_msg = "REFUSE"
        conn.send(ref_msg.encode('ascii'))
        conn.close()
        return

    #else the client is accepted
    acc_msg = "ACCEPT"
    conn.send(acc_msg.encode('ascii'))

    GlobalVars.global_lock.acquire()
    print(f"Connection with Client {client_id} started")

    #check is user exists yet
    user_exists = False
    the_user = None
    for user in GlobalVars.all_users:
        if user.client_id == client_id:
            user_exists = True
            the_user = user
            break
    #create user if first time loging in
    if not user_exists:
        the_user = User(client_id, conn)
        GlobalVars.all_users.append(the_user)
    the_user.isConnected = True
    the_user.connection = conn

    #update user on any msgs in the system that they havent seen
    update_user(the_user)
    GlobalVars.global_lock.release()

    while True: 
        data = conn.recv(1024).decode() 
        if not data: 
            GlobalVars.global_lock.acquire()
            print(f'Connection With Client {client_id} closed') 
            the_user.isConnected = False
            the_user.connection = None
            GlobalVars.global_lock.release()
            break
        else:
            GlobalVars.global_lock.acquire()
            the_msg = Message(client_id, data, GlobalVars.next_msg_id)
            print(the_msg)
            GlobalVars.next_msg_id = GlobalVars.next_msg_id + 1
            GlobalVars.all_msgs.append(the_msg)
            push_messages()
            GlobalVars.global_lock.release()
    conn.close() 

#instance of a msg in the system
#stored so that users not online can get them later
class Message():
    def __init__(self, the_sender, the_text, the_msg_id):
        self.sender = the_sender
        self.text = the_text
        self.msg_id = the_msg_id

    def __str__(self):
        the_str = "\nPrinting Received Message:\n"
        the_str += "Client ID - " + self.sender + "\n"
        the_str += "Message ID - " + str(self.msg_id) +"\n"
        the_str += "Text - " + self.text + "\n"
        return the_str

#instance of a user in the system
#keeps track of thei connection and messages seen
class User():
    def __init__(self, the_id, the_conn):
        self.client_id = the_id
        self.isConnected = True
        self.connection = the_conn
        self.last_msg_id_seen = -1

#lock is already acquired when this is called
def push_messages():
    for user in GlobalVars.all_users:
        push_to_user(user)
    return

def push_to_user(user):
    if not user.isConnected:
        return
    last_msg = user.last_msg_id_seen
    if last_msg < GlobalVars.next_msg_id -1:
        msg = GlobalVars.all_msgs[last_msg+1]
        user.last_msg_id_seen = msg.msg_id
        if msg.sender == user.client_id:
            return
        the_msg = str(msg.sender) + ": " + msg.text
        user.connection.send(the_msg.encode('ascii'))

#update a single user becaue they just logged on
#only send new msgs that they have seen
def update_user(the_user):
    last_msg = the_user.last_msg_id_seen
    if last_msg < GlobalVars.next_msg_id - 1:
        for msg in GlobalVars.all_msgs:#TODO can we start at index of last msg
            if msg.msg_id > last_msg:
                break_text = str(msg.sender)+": "+msg.text+"msg_break789"
                the_user.connection.send(break_text.encode('ascii'))
                the_user.last_msg_id_seen = msg.msg_id
    #this text signifies the end of new messages 
    break_text = "break1234567890"
    the_user.connection.send(break_text.encode('ascii'))
    return


if __name__ == "__main__":
    main()
