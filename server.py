import sys
import socket
from _thread import *
import threading 


#since python doesnt have struct and i need to C
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

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", int(port_arg)))
    sock.listen(len(clients_list)+5)
    try:
        while True:
            conn, addr = sock.accept()
            start_new_thread(thread_func, (conn,))
    
    except (KeyboardInterrupt, SystemExit):
        print("exiting. closing connections.")
        cleanup_connections()
        sys.exit()
    return

def cleanup_connections():
    for user in GlobalVars.all_users:
        if user.isConnected:
            user.connection.close()

def thread_func(conn): 
    client_id = conn.recv(1024).decode()
    if client_id not in GlobalVars.all_client_ids:
        GlobalVars.global_lock.acquire()
        print(f"Refusing connection with client {client_id}")
        GlobalVars.global_lock.release()
        ref_msg = "REFUSE"
        conn.send(ref_msg.encode('ascii'))
        conn.close()
        return


    acc_msg = "ACCEPT"
    conn.send(acc_msg.encode('ascii'))

    GlobalVars.global_lock.acquire()
    print(f"Connection with Client {client_id} started")
    user_exists = False
    the_user = None
    for user in GlobalVars.all_users:
        if user.client_id == client_id:
            user_exists = True
            the_user = user
            break

    if not user_exists:
        the_user = User(client_id, conn)
        GlobalVars.all_users.append(the_user)
    the_user.isConnected = False
    the_user.connection = conn

    push_messages()
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

class User():
    def __init__(self, the_id, the_conn):
        self.client_id = the_id
        self.isConnected = True
        self.connection = the_conn
        self.last_msg_id_seen = -1


def push_messages():
    return

if __name__ == "__main__":
    main()
