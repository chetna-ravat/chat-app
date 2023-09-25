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


def isMsgFormatCorrect(msg):
	# [{data_time}]SEPARATOR{name}SEPARATOR{msg}
	return len(msg.split(SEPARATOR)) == 3

def getUserName(msg):
	return msg.split(SEPARATOR)[1]

def isUserRegistering(msg):
	msgs = msg.split(SEPARATOR)
	return msgs[-1].strip() == "\x1b[39m"

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
				print(f"{PLUS}Registering {name}{Fore.RESET}")
				msg += "Joined"
			else:
				print(f"msg received from {Fore.BLUE}{name}{Fore.RESET}")
			msg = msg.replace(SEPARATOR, ": ")
		
		clientSockets = clientSocketToName.keys()	
		for cs in clientSockets:
			if cs != clientSocket:
				cs.send(msg.encode())
	

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

