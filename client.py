import socket
import random
import os
from dotenv import load_dotenv
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Load environment variables
load_dotenv()

# Server connection information
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = int(os.getenv('SERVER_PORT'))


# initalize colors
init()

# Colors list to choose from for client msg
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# Randomly choose color for colors list
clientColor = random.choice(colors)

SEPARATOR = "<SEP>"
QUITE='q'

def formatMessage(name, msg):
	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	return f"{clientColor}[{now}]{SEPARATOR}{name}{SEPARATOR}{msg}{Fore.RESET}"

def sendMessage(name, msg):
	msg = formatMessage(name, msg)
	s.send(msg.encode())

def receiveMessage():
	return s.recv(1024).decode()

def processServerMessages():
	while True:
		msg = receiveMessage()
		if msg:
			print("\n" + msg)
			print("> ")


def startChat():
	# Register user
	while True:
		name = input("Register your name: ").strip()
		if name.lower() == QUITE:
			return
		if name != "":
			sendMessage(name, "")
			break

	print(f"Thank you {name} for registering on our platfrom.")
	print("You can now start chatting")

	# start sending messages	
	while True:
		msg = input("> ").strip()
		if msg.lower() == QUITE:
			return
		if msg != "":
			sendMessage(name, msg)

if __name__ == "__main__":
	# Create connection to server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(f"[*] Connecting to {SERVER_IP}:{SERVER_PORT}...")
	s.connect((SERVER_IP, SERVER_PORT))
	print("[+] Connected.")	

	# make a thread that listens for messages to this client & print them
	t = Thread(target=processServerMessages)
	# make the thread daemon so it ends whenever the main thread ends
	t.daemon = True
	# start the thread
	t.start()
	
	startChat()	
	
# close the socket
s.close()
