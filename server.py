import os
import socket
from threading import Thread
from dotenv import load_dotenv
from colorama import Fore, init, Back

# initialize colors
init()

# Colors
PLUS=Fore.GREEN
LISTENING=Fore.LIGHTYELLOW_EX
CLOSE=Fore.RED

# Load environment variables
load_dotenv()

# Server connection information
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = int(os.getenv('SERVER_PORT'))

SEPARATOR = "<SEP>"

# Unknown name for client
UNKNOWN = "Unknown"

# Client name to socket map
clientSocketToName = dict()

# Unicode color code
COLOR_UNICODE="\x1b[39m"

def isMsgFormatCorrect(msg):
	# [{data_time}]SEPARATOR{name}SEPARATOR{msg}
	return len(msg.split(SEPARATOR)) == 3

def getUserName(msg):
	return msg.split(SEPARATOR)[1]

def isUserRegistering(msg):
	msgs = msg.split(SEPARATOR)
	return msgs[-1].strip() == COLOR_UNICODE

def isUserQuiting(msg):
	msgs = msg.split(SEPARATOR)
	return msgs[-1].strip().lower() == f"quit{COLOR_UNICODE}"

def getUserQuitingMsg(msg):
	msgs = msg.split(SEPARATOR)
	msgs[-1] = "Left"
	return f"{SEPARATOR}".join(msgs)	

def handleClient(clientSocket):
	while True:
		try:
			msg = clientSocket.recv(1024).decode()
		except Exception as e:
			del clientSocketToName[clientSocket]
		# only process correct msg
		if isMsgFormatCorrect(msg):
			name = getUserName(msg)
			# Update client name
			if clientSocketToName[clientSocket] == UNKNOWN:
				clientSocketToName[clientSocket] = name

			if isUserRegistering(msg):
				print(f"{PLUS}[++]Registering {name}{Fore.RESET}")
				msg += "Joined"
			elif isUserQuiting(msg):
				print(f"{CLOSE}[--]Leaving {name}{Fore.RESET}")
				# remove client from the map
				del clientSocketToName[clientSocket]
				msg = getUserQuitingMsg(msg)
			else:
				print(f"msg received from {Fore.BLUE}{name}{Fore.RESET}")
			msg = msg.replace(SEPARATOR, ": ")
		
		# clientSocketToName map can get change in middle of looping
		# if some client leaves or new client gets joined.
		# This will lead us to exceptopn: "Dictionary changes the size during
		# iteration. To avoid this copy keys into tuple and iterator over it.
		clientSockets = tuple(clientSocketToName.keys())
		for cs in clientSockets:
			if cs != clientSocket:
				try:
					cs.send(msg.encode())
				except socket.error as e:
					print(f"Socket error encountered for {clientSocketToName[cs]}")
				except IOError as e:
					if e.errno == errno.EPIPE:
						print(f"client pipe is broken")
					else:
						print(f"Unknown error {e} encountered")
	

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Allow reusablity of TCP connection
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Bind server ip and port to socket
	s.bind((SERVER_IP, SERVER_PORT))
	# start listening 
	s.listen()
	print(f"{LISTENING}Listening on {SERVER_IP}:{SERVER_PORT} ...{Fore.RESET}")
	

	while True:
		# Keep listening for client connection
		clientSocket, clientIpAddress = s.accept()
		print(f"{PLUS}[+]{Fore.RESET} New client from {clientIpAddress} connected.")
		
		clientSocketToName[clientSocket] = UNKNOWN

		# start new thread to handle new client
		t = Thread(target=handleClient, args=(clientSocket,))
		t.daemon = True
		t.start()

for cs, name in clientSocketToName.items():
	print(f"{CLOSE}Closing connection of client '{name}'...{Fore.RESET}")
	cs.close()

print("{CLOSE}Shutting down server connection{Fore.RESET}")
# close server connection
s.close()

