import requests
import urllib3

urllib3.disable_warnings()
try:
	
	response = requests.get("https://d22d-2800-98-1126-cfb-d010-a6d4-8cd9-5013.ngrok-free.app/test", verify = False)
	
	print(response.status_code)

except:
	
	print("Error")	

