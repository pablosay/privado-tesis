import requests

import urllib3

from dotenv import load_dotenv

import os

load_dotenv()

urllib3.disable_warnings()

headers = {
	"authorization": f"Bearer {os.getenv('AUTHORIZATION_TOKEN')}",
	"Content-Type": "application/json"
}

def classify(image, bbox, model, ip):
	
	json_body_request = {'image': image, 'bbox': bbox, 'model': model}
	
	response_classification = requests.post(ip + '/classify', json = json_body_request,  verify = False)
	
	return response_classification.json()
	
	
def detect(image, ip):
	
	json_body_request = {'image': image}
	
	response_detection = requests.post( ip + '/predictface', json = json_body_request,  verify = False)
	
	return response_detection.json()


def spoofdetect(image, ip):
	
	json_body_request = {'image': image}
	
	response_spoof = requests.post( ip + '/spoofdetect', json = json_body_request, verify = False)
	
	return response_spoof.json()
	
	
def register_entry(name, time):
	
	request_data = { 'hour': time.hour, 'minute': time.minute, 'day': time.day, 'month':time.month, 'year':time.year, 'name':name}
	
	response = requests.post('https://privadoapp-production.up.railway.app/log/entry', json =request_data, headers=headers)
	
	return response.json()
	
	
def register_intruder(name, time, image):
	
	request_data = { 'hour': time.hour, 'minute': time.minute, 'day': time.day, 'month':time.month, 'year':time.year, 'name':name, 'image': image}
	
	response = requests.post('https://privadoapp-production.up.railway.app/log/intruder', json =request_data,  headers=headers)
	
	return response.json()



