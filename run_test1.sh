#!/bin/bash
echo "starting Test 1: Alice sends a message, Chad and Bob come online after 5 seconds to see it."

echo "Starting server in background."
PORT_NUM=$1
SERVER_IP=$2
python3 -u server.py -client_ids Alice,Bob,Chad -port $PORT_NUM &

sleep 3
echo ""
echo "Bringing Alice online to send message from test1_alice_input.txt"
python3 -u client.py -client_id Alice -server_ip $2 -port $PORT_NUM < test1_alice_input.txt
echo "Done with Alice"

sleep 5
echo ""
echo "Bringing Bob Online"
echo "quit" | python3 -u client.py -client_id Bob -server_ip $2 -port $PORT_NUM
echo "Done with Bob"

echo ""
echo "Bringing Chad Online"
echo "quit" | python3 -u client.py -client_id Chad -server_ip $2 -port $PORT_NUM
echo "Done with Chad"

echo "Killing server in the background"
killall python3
