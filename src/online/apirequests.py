import requests

def classify(image, bbox, model):
	
	json_body_request = {'image': image, 'bbox': bbox, 'model': model}
	
	response_classification = requests.post('http://192.168.1.6:1500/classify', json = json_body_request)
	
	return response_classification.json()
	
	
def detect(image):
	
	json_body_request = {'image': image}
	
	response_classification = requests.post('http://192.168.1.6:1500/predictface', json = json_body_request)
	
	return response_classification.json()

