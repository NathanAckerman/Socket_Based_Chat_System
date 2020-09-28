#!/bin/bash
echo "starting Test 4: Alice logs in, sends a message, logs out, logs in, sends a message, bob logs in and sees two messages (the same ones), then bob sends a message, then alice logs in and sees it"

echo "Starting server in background."
PORT_NUM=$1
SERVER_IP=$2
python3 -u server.py -client_ids Alice,Bob -port $PORT_NUM &

sleep 3
echo ""
echo "Bringing Alice online to send message from test3_alice_input.txt"
python3 -u client.py -client_id Alice -server_ip $2 -port $PORT_NUM < test3_alice_input.txt
echo "Done with Alice 1"

sleep 3
echo ""
echo "Bringing Alice online to send second message from test3_alice_input.txt"
python3 -u client.py -client_id Alice -server_ip $2 -port $PORT_NUM < test3_alice_input.txt
echo "Done with Alice 2"

sleep 3
echo ""
echo "Bringing Bob Online"
python3 -u client.py -client_id Bob -server_ip $2 -port $PORT_NUM < test4_bob_input.txt
echo "Done with Bob"

sleep 3
echo ""
echo "Bringing Alice online to see message from bob"
echo "quit" | python3 -u client.py -client_id Alice -server_ip $2 -port $PORT_NUM
echo "Done with Alice 3"
echo "Killing server in the background"
killall python3
