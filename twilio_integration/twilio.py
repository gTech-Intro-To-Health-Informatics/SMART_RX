import os
import json
import uuid
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


def generate_conversation_id():
    """Generate a unique conversation ID."""
    return str(uuid.uuid4())


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


def send_text_with_conversation(phone_number, conversation_id, conversation_link, use_whatsapp=False):
    """Send a text or WhatsApp message with the conversation ID and link via Twilio."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message_body = f"Your conversation ID: {conversation_id}\nLink: {conversation_link}"
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
        raise Exception(f"Failed to send message: {str(e)}")


def create_and_send_conversation(phone_number, use_whatsapp=False):
    """Generate conversation details, save them, and send them via SMS or WhatsApp."""
    # Load existing conversations
    conversations = load_conversations()

    # Check if a conversation already exists for the phone number
    existing_conversation = find_conversation_by_phone(phone_number, conversations)
    if existing_conversation:
        # Send the existing conversation details
        sms_response = send_text_with_conversation(
            phone_number,
            existing_conversation["conversation_id"],
            existing_conversation["conversation_link"],
            use_whatsapp=use_whatsapp
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
    sms_response = send_text_with_conversation(phone_number, conversation_id, conversation_link, use_whatsapp=use_whatsapp)

    # Return the full response including phone number
    return {
        "phone_number": phone_number,
        "conversation_id": conversation_id,
        "conversation_link": conversation_link,
        **sms_response,
    }

# Example usage
if __name__ == "__main__":
    phone_number = "+1234567890"  # Replace with the recipient's phone number
    use_whatsapp = True  # Set to True to send via WhatsApp, False for SMS
    response = create_and_send_conversation(phone_number, use_whatsapp=use_whatsapp)
    print(response)
