import requests

def classify(image, bbox, model, ip):
	
	json_body_request = {'image': image, 'bbox': bbox, 'model': model}
	
	response_classification = requests.post( ip + '/classify', json = json_body_request)
	
	return response_classification.json()
	
	
def detect(image, ip):
	
	json_body_request = {'image': image}
	
	response_classification = requests.post(ip + '/predictface', json = json_body_request)
	
	return response_classification.json()


def spoofdetect(image, ip):
	
	json_body_request = {'image': image}
	
	response_spoof = requests.post(ip + '/spoofdetect', json = json_body_request)
	
	return response_spoof.json()

