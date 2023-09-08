import time
import subprocess
import socket
import argparse
from art import *

def check_internet_connection():
	
	try:
		
		socket.create_connection(("www.google.com", 80))
		
		return True
	
	except OSError:
		
		return False
		
		
def main(ip):
	
	while True:
		
		if check_internet_connection():
			
			print("Internet connection.")
			
			subprocess.run(['python', 'src/main_online.py', ip])
			
		else:
			
			print("No internet connection, trying local processing.")
			
			subprocess.run(['python', 'src/main_offline.py'])
			
	time.sleep(5)
	
if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description = 'Main file: Decides which script runs.')
	
	parser.add_argument('ip', type = str, help ='IP of the backend')
	
	args = parser.parse_args()
	
	texto = text2art("PRIVADO 23")
	
	print(texto)
	
	print("Pablo Alejandro Say Cutz, 19001434 \n")
	
	main(args.ip)
