#!/bin/bash
echo "starting Test 1: Alice sends a message, Chad and Bob come online after 5 seconds to see it."

echo "Starting server in background. Server output will go to server_output.txt"
PORT_NUM=22104
python3 server.py -client_ids 1,2,3 -port $PORT_NUM &

sleep 3
echo ""
echo "Bringing Alice online to send message from test1_alice_input.txt"
python3 client.py -client_id 1 -server_ip 127.0.0.1 -port $PORT_NUM < test1_alice_input.txt
echo "Done with Alice"

sleep 5
echo ""
echo "Bringing Bob Online"
echo "quit" | python3 client.py -client_id 2 -server_ip 127.0.0.1 -port $PORT_NUM
echo "Done with Bob"

echo ""
echo "Bringing Chad Online"
echo "quit" | python3 client.py -client_id 3 -server_ip 127.0.0.1 -port $PORT_NUM
echo "Done with Chad"

