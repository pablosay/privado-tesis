import os
from dotenv import load_dotenv
load_dotenv()

from twilio.rest import Client

account_sid = os.getenv('TWILIO_CID')

auth_token = os.getenv('TWILIO_TOKEN')

client = Client(account_sid, auth_token)
message = client.messages.create(from_='whatsapp:+14155238886', body='Your appointment is coming up on July 21 at 3PM', to='whatsapp:+50230724754')
print(message)
