#### NOTE: Please update the OpenAPI apikey and .env Twilio API Keys before running the server

### To run the app: 
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Text Integrations
```
/POST 
/send-conversation-link/{phone_number}
- Saves the conversation_id, conversation_link and patient_phone number in the json file
- Send the text message with conversation_id, conversation_link to the patient_phone number 
- Checks if the phone number already exist in json file before creating a new one, otherwise fetch the existing one. 
```

#### Text integration Usage
```
curl --location --request POST 'localhost:8000/send-conversation-link/[your_phone_number]]'
```
 
#### Text Challenges
```
- Tried Twilio + Twilio Whatsapp + Ultramessage + TextBelt
- Twilio Issue: All U.S. SMS and MMS messages from unregistered 10DLC phone numbers are now blocked (Additional cost and time involved for registration.)
    - $0.035 cost involved per text ($20 loaded in the wallet)
- Twilio Whatsapps Issue: Business Verification required + can send whats app text to only added numbers
- Ultra Message Issue: Can send whatsapp text to only added numbers
- TextBelt: Can not send links in test (Used (dot) notation for links for now)
    - Text Messages Working (Currently account in verification for sending link as well)
    - Current Quota: $5 (200 Texts)
    - Check Quota: https://textbelt.com/quota/<api_key>
```

#### Add ons: 
```
- Unique uuid to track conversation and conversation links    
- Added environment config file + variables  
```