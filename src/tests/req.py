import requests

import urllib3

from datetime import datetime

urllib3.disable_warnings()

def register_entry(name, time):
	
	request_data = { 'hour': time.hour, 'minute': time.minute, 'day': time.day, 'month':time.month, 'year':time.year, 'name':name}
	
	response = requests.post('http://192.168.1.17:1300/log/entry', json =request_data,  verify = False)
	
	return response.json()

def register_intruder(name, time, image):
	
	request_data = { 'hour': time.hour, 'minute': time.minute, 'day': time.day, 'month':time.month, 'year':time.year, 'name':name, 'image': image}
	
	response = requests.post('http://192.168.1.17:1300/log/intruder', json =request_data,  verify = False)
	
	return response.json()


response = register_entry('PabloSay', datetime.now())

print(response['message'])
