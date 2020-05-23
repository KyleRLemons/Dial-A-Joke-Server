'''
This is the dial-a-joke service.
Your client can connect and request jokes via the following protocol.
Each request consists of two parts:
	1) 3 byte long command
	2) 3 byte long argument

	The command can be Q, A or X
	Q requests the setup for the joke
	A requests the punch line
	X is a disconnect message

	The argument is an integer within the range of the number of jokes
	available, beginning with joke 0

	So an example command is: "Q  1  " which requests the setup for
	joke 1, the response will be a bytestream containing the joke in utf-8.
	"X  0  " would be a signal to disconnect from the server.

'''
import socket
import time
from _thread import *
import threading

PORT = 1234
NUM_CONNECTIONS = 2
CMD_LEN = 3
ARG_LEN = 3
commands = ('Q', 'A', 'X')
jokes = ({'Q': 'What time do you visit the dentist?',
          'A': 'Tooth-hurty.'},
         {'Q': 'What\'s the best thing about Switzerland?',
          'A': 'I don\'t know, but the flag is a big plus.'},
         {'Q': 'Helvetica and Comic Sans walk into a bar, the bartender says....',
          'A': 'Get out of here, we don\'t serve your type!'})


# thread function
def threaded(c):
    try:
        c.send(bytes(f"Welcome to the dial-a-joke server, you may request jokes from 0 to {len(jokes) - 1}", "utf-8"))

        cmd = ''
        while cmd != 'X':
            # Read the header and extract the content length.
            cmd = c.recv(CMD_LEN)
            arg = c.recv(ARG_LEN)

            if cmd and arg:
                cmd = cmd.decode("utf-8").strip()
                arg = int(arg.decode("utf-8"))
            else:
                print('Bye')
                break

            if not cmd in commands:
                c.send(bytes("Invalid command '" + cmd + "'", 'utf-8'))
            if arg < 0 or arg >= len(jokes):
                c.send(bytes('Argument out of bounds, must be postive integer less than ' + len(jokes), 'utf-8'))

            if cmd == 'X':
                data = 'Good bye, thanks for using dial a joke.'
            else:
                data = jokes[arg][cmd]

            # Send data back to user.
            print('Send:', data)
            c.send(data.encode('utf-8'))

        # connection closed
        print('Disconnected')
        c.close()
    except:
        print('Error, quitting')
        if c: c.close()


# SOCK_DGRAM for UDP, STREAM for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#I HAD TO CHANGE THE S.BIND TO MY LINK LOCAL IPV6 ADDRESS SO THIS MAY NOT WORK FOR YOU
s.bind(('127.0.0.1', PORT))
# Listen, queues N simultaneous connections
s.listen(NUM_CONNECTIONS)

print('Listening on port', PORT)

while True:
    clientsocket, addr = s.accept()
    print('Connected to :', addr[0], ':', addr[1])

    start_new_thread(threaded, (clientsocket,))


