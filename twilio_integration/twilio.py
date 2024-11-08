import os
import json
import uuid
import requests
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials and other settings from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
BASE_CONVERSATION_URL = os.getenv("BASE_CONVERSATION_URL")
CONVERSATION_STORAGE_FILE = os.getenv("CONVERSATION_STORAGE_FILE", "conversations.json")

# UltraMsg credentials
ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

# Textbelt API
TEXTBELT_API_URL = "https://textbelt.com/text"
TEXTBELT_API_KEY = os.getenv("TEXTBELT_API_KEY")


def generate_conversation_id():
    """Generate a unique conversation ID."""
    return str(uuid.uuid4())[:4]

def load_conversations():
    """Load existing conversations from the JSON file."""
    if os.path.exists(CONVERSATION_STORAGE_FILE):
        with open(CONVERSATION_STORAGE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


def save_conversations(conversations):
    """Save all conversations back to the JSON file."""
    with open(CONVERSATION_STORAGE_FILE, "w") as file:
        json.dump(conversations, file, indent=4)


def find_conversation_by_phone(phone_number, conversations):
    """Find a conversation by phone number."""
    for conversation_id, details in conversations.items():
        if details["phone_number"] == phone_number:
            return details
    return None


def save_conversation(phone_number, conversation_id, conversation_link):
    """Save the conversation data (phone number, ID, and link) to a JSON file."""
    conversations = load_conversations()

    # Add the new conversation
    conversations[conversation_id] = {
        "phone_number": phone_number,
        "conversation_id": conversation_id,
        "conversation_link": conversation_link,
    }

    # Save back to file
    save_conversations(conversations)


def obfuscate_link(link):
    """Obfuscate the link to avoid detection as a URL."""
    return link.replace(".", "[dot]").replace("https://", "")


def send_ultramsg_message(phone_number, message_body):
    """Send a WhatsApp message using UltraMsg."""
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "to": phone_number,
        "body": message_body,
        "token": ULTRAMSG_TOKEN
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return {"message": "Message sent successfully!", "sid": response.json().get("id")}
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to send message via UltraMsg: {str(e)}")


def send_textbelt_message(phone_number, message_body):
    """Send an SMS message using Textbelt."""
    payload = {
        "phone": phone_number,
        "message": message_body,
        "key": TEXTBELT_API_KEY
    }

    try:
        response = requests.post(TEXTBELT_API_URL, data=payload)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("success"):
            return {"message": "Message sent successfully via Textbelt!", "sid": response_data.get("id")}
        else:
            raise Exception(f"Textbelt error: {response_data.get('error')}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to send message via Textbelt: {str(e)}")


def send_text_with_conversation(phone_number, conversation_link, use_whatsapp=False, use_ultramsg=False, use_textbelt=False):
    """Send a text or WhatsApp message with just the obfuscated link."""
    # Obfuscate the conversation link
    obfuscated_link = obfuscate_link(conversation_link)

    # Create the message body
    message_body = f"{obfuscated_link}"

    if use_ultramsg:
        return send_ultramsg_message(phone_number, message_body)

    if use_textbelt:
        return send_textbelt_message(phone_number, message_body)

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    from_number = TWILIO_WHATSAPP_NUMBER if use_whatsapp else TWILIO_PHONE_NUMBER
    to_number = f"whatsapp:{phone_number}" if use_whatsapp else phone_number

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        return {"message": "Message sent successfully!", "sid": message.sid}
    except Exception as e:
        raise Exception(f"Failed to send message via Twilio: {str(e)}")


def create_and_send_conversation(phone_number, use_whatsapp=False, use_ultramsg=False, use_textbelt=False):
    """Generate conversation details, save them, and send just the link via SMS or WhatsApp."""
    # Load existing conversations
    conversations = load_conversations()

    # Check if a conversation already exists for the phone number
    existing_conversation = find_conversation_by_phone(phone_number, conversations)
    if existing_conversation:
        # Send the existing conversation link
        sms_response = send_text_with_conversation(
            phone_number,
            existing_conversation["conversation_link"],
            use_whatsapp=use_whatsapp,
            use_ultramsg=use_ultramsg,
            use_textbelt=use_textbelt
        )

        # Return the existing conversation details along with the SMS/WhatsApp response
        return {
            "phone_number": existing_conversation["phone_number"],
            "conversation_id": existing_conversation["conversation_id"],
            "conversation_link": existing_conversation["conversation_link"],
            **sms_response,
        }

    # Generate a new conversation ID and link
    conversation_id = generate_conversation_id()
    conversation_link = f"{BASE_CONVERSATION_URL}/{conversation_id}"

    # Save the new conversation details
    save_conversation(phone_number, conversation_id, conversation_link)

    # Send the details via SMS or WhatsApp
    sms_response = send_text_with_conversation(
        phone_number, conversation_link, use_whatsapp=use_whatsapp, use_ultramsg=use_ultramsg, use_textbelt=use_textbelt
    )

    # Return the full response including phone number and conversation ID
    return {
        "phone_number": phone_number,
        "conversation_id": conversation_id,
        "conversation_link": conversation_link,
        **sms_response,
    }