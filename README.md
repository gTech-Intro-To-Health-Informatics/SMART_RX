### To run the app: 
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Twilio Integrations
```
/POST 
/send-conversation-link/{phone_number}
- Saves the conversation_id, conversation_link and patient_phone number in the json file
- Send the text message with conversation_id, conversation_link to the patient_phone number 
- Checks if the phone number already exist in json file before creating a new one, otherwise fetch the existing one. 
```

#### Twilio integration Usage
```
curl --location --request POST 'localhost:8000/send-conversation-link/[your_phone_number]]'
```
 
#### Twilio Challenges
```
- All U.S. SMS and MMS messages from unregistered 10DLC phone numbers are now blocked (Additional cost and time involved for registration.)
- $0.035 cost involved per text ($20 loaded in the wallet)
- Whatsapp Integration instead of regular text message
- Added environment config file + variables  
```