"""
A port scanner is a tool that scans a range of network ports on a target machine to determine which ports are open and can be used to establish a network connection.

Please note that you should use this script only on systems and networks that you have permission to scan.

To test this script you can start a local python server, by default on port 8000:
`python -m http.server`

then run this script to scan the available ports on localhost.
"""

# the socket library allows us to handle network connections
import socket

def scan_port(host, port):
    # print(f'Attempting connection to port #{port}...')
    try:
        # connection
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set a timeout for connection attempt
        client.settimeout(1)

        # attempt connection
        client.connect((host, port))

        print(f'Port {port} is open')

        client.close()
    except (socket.timeout, ConnectionRefusedError):
        print(f'Port {port} closed')

# set parameters
target_host = '127.0.0.1' # change this
start_port = 7990
end_port = 8003

# scan range
for port in range(start_port, end_port):
    scan_port(target_host, port)