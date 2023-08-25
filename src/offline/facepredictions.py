import cv2
from ultralytics import YOLO

facedetectionmodel = YOLO('../../data/models/best.pt')

def faceprediction(image):
	
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, (640,640))
	
	prediction = facedetectionmodel(rgb, conf = 0.75, imgsz = 640, verbose = False, device = 'cpu')
	
	if len(prediction) > 0:
		
		return prediction[0].boxes.data.numpy()
		
	return []
