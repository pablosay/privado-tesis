import time
import subprocess
import socket
from art import *

def check_internet_connection():
	
	try:
		
		socket.create_connection(("www.google.com", 80))
		
		return True
	
	except OSError:
		
		return False
		
		
def main():
	
	while True:
		
		if check_internet_connection():
			
			print("Internet connection.")
			
			subprocess.run(['python', 'src/main_online.py'])
			
		else:
			
			print("No internet connection, trying local processing.")
			
			subprocess.run(['python', 'src/main_offline.py'])
			
	time.sleep(5)
	
if __name__ == '__main__':
	
	texto = text2art("PRIVADO 23")
	
	print(texto)
	
	print("Pablo Alejandro Say Cutz, 19001434 \n")
	
	main()
