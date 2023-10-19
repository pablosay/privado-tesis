import requests

import urllib3

urllib3.disable_warnings()

def classify(image, bbox, model, ip):
	
	json_body_request = {'image': image, 'bbox': bbox, 'model': model}
	
	response_classification = requests.post('https://' + ip + ':1500/classify', json = json_body_request,  verify = False)
	
	return response_classification.json()
	
	
def detect(image, ip):
	
	json_body_request = {'image': image}
	
	response_detection = requests.post('https://' + ip + ':1500/predictface', json = json_body_request,  verify = False)
	
	return response_detection.json()


def spoofdetect(image, ip):
	
	json_body_request = {'image': image}
	
	response_spoof = requests.post('https://' + ip + ':1500/spoofdetect', json = json_body_request, verify = False)
	
	return response_spoof.json()
	
	
def register_entry(name, time):
	
	request_data = { 'hour': time.hour, 'minute': time.minute, 'day': time.day, 'month':time.month, 'year':time.year, 'name':name}
	
	response = requests.post('http://192.168.1.17:1300/log/entry', json =request_data)
	
	return response.json()
	
	
def register_intruder(name, time, image):
	
	request_data = { 'hour': time.hour, 'minute': time.minute, 'day': time.day, 'month':time.month, 'year':time.year, 'name':name, 'image': image}
	
	response = requests.post('http://192.168.1.17:1300/log/intruder', json =request_data,  verify = False)
	
	return response.json()



