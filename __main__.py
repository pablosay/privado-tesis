import time
import subprocess
import requests
import argparse
from art import *
from src.utils.software import get_ip, there_is_connection, check_internet_connection

		
def main():
	
	while True:
		
		if check_internet_connection():
			
			ip = get_ip()
			
			print("There is internet connection")
			
			print("Processing server IP: ", ip)
			
			if there_is_connection(ip):
				
				print("Connection to ", ip)
				
				subprocess.run([ 'python', 'src/main_online.py', ip])
			
			else:
				
				print("Processing server is unaviable.")
			
				subprocess.run(['python', 'src/main_offline.py'])
				
			
		else:
			
			print("No internet connection, trying local processing.")
			
			subprocess.run(['python', 'src/main_offline.py'])
			
		time.sleep(5)
	
if __name__ == '__main__':
	
	texto = text2art("PRIVADO 23")
	
	print(texto)
	
	print("Pablo Alejandro Say Cutz, 19001434 \n")
	
	main()
