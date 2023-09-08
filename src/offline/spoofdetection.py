import cv2
from ultralytics import YOLO

antispoofmodel = YOLO('/home/pablosay21/Documentos/privado-tesis/data/models/antispoof.pt')

def spoofpredict(image):
	
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, (640,640))
	
	prediction = antispoofmodel(rgb, conf = 0.75, imgsz = 640, verbose = False, device = 'cpu')
	
	if len(prediction) > 0:
		
		return prediction[0].boxes.data.numpy()
		
	return []
