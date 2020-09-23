#!/bin/bash
echo "starting Test 2: A,B, and C come online. B sends a message, then A sends a msg, then D comes online but is not given any messages"
echo "Because the output from multiple background processes is hard to parse for users staying online, the output of a message that was received by a user is after something of the form client_id's console: "

echo "Starting server in background."
PORT_NUM=$1
SERVER_IP=$2
python3 -u server.py -client_ids Alice,Bob,Chad -port $PORT_NUM &

sleep 3
echo ""
echo "Bringing Alice online"
python3 -u client.py -client_id Alice -server_ip $2 -port $PORT_NUM < test2_alice_input.txt &

sleep 1
echo ""
echo "Bringing Chad Online"
echo "wait" | python3 -u client.py -client_id Chad -server_ip $2 -port $PORT_NUM &

sleep 1
echo ""
echo "Bringing Bob Online"
echo "Bob will send message first"
python3 -u client.py -client_id Bob -server_ip $2 -port $PORT_NUM < test2_bob_input.txt &
sleep 1
echo "Now alice needs to send her message"
sleep 2
sleep 2
sleep 2
sleep 2
echo "Killing server in the background"
killall python3
