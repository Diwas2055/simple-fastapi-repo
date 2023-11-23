import asyncio
import requests
from twilio.rest import Client
from twilio.base import exceptions as twilio_exceptions


def get_balance_telynx():
    telnyx_api_key = ""
    """Get the balance of the Telynx account."""
    url = "https://api.telnyx.com/v2/balance"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {telnyx_api_key}",
    }
    response = requests.get(url=url, headers=headers)
    r_json = response.json()
    return r_json


def get_balance_twilio():
    TWILIO_ACCOUNT_SID = ""
    TWILIO_AUTH_TOKEN = ""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    balance = client.balance.fetch().balance
    return balance


def get_current_twilio():
    try:
        balance = 0
        TWILIO_ACCOUNT_SID = ""
        TWILIO_AUTH_TOKEN = ""
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        try:
            response = client.balance.fetch()
            balance = response.balance
            return balance
        except twilio_exceptions.TwilioRestException as err:
            # logger.info("Error in getting balance from twilio", err)
            return 0
    except twilio_exceptions.TwilioRestException as e:
        print(f"Error: {e}")
        return None


print(get_current_twilio())
