import json
from datetime import datetime
from faker import Faker
import time

import requests

fake = Faker()

# Generate fake data
subject = "Error Notification"
status_code = fake.random_int(min=400, max=500)
device_id = fake.uuid4()
message = fake.sentence()


# Example request object (you may need to adjust this based on your actual code)
class FakeRequest:
    def __init__(self, method, path, user_agent, user=None):
        self.method = method
        self.path = path
        self.user_agent = user_agent
        self.user = user


# Example request and status code
request = FakeRequest("GET", "/example/path", "Mozilla/5.0")
status_code = fake.random_int(min=400, max=500)

# Construct attachments
attachments = [
    {
        "title": subject,
        "color": "danger",
        "fields": [
            {"title": "Level", "value": "ERROR", "short": True},
            {"title": "Server Name", "value": f"{fake.word()}-local", "short": True},
            {
                "title": "Method",
                "value": request.method if request else "No Request",
                "short": True,
            },
            {
                "title": "Path",
                "value": request.path if request else "No Request",
                "short": True,
            },
            {
                "title": "User",
                "value": "Anonymous",
                "short": True,
            },
            {"title": "Status Code", "value": status_code, "short": True},
            {"title": "Date", "value": datetime.utcnow().strftime("%c"), "short": True},
            {
                "title": "GET Params",
                "value": json.dumps({"param1": "value1", "param2": "value2"}),
                "short": True,
            },
            # Adjust fake GET params
            {
                "title": "POST Data",
                "value": fake.text(),
                "short": True,
            },
            {
                "title": "Agent",
                "value": request.user_agent
                if request and request.user_agent
                else "No Request",
                "short": True,
            },
        ],
    },
]

# Add Error Details
attachments.append(
    {
        "channel": "dialaxy-log",
        "color": "danger",
        "title": "Error Details",
        "text": message,
        # "ts": time.time(),
        "footer": f"{subject} | {time.time()}",
    }
)

main_text = f"Error at {time.strftime('%A, %d %b %Y %H:%M:%S +0000', time.gmtime())}"

# Create the final data payload
data = {
    "payload": json.dumps({"channel": "dialaxy-log", "attachments": attachments}),
}

# Print the generated data

import requests

data = {
    "main_text": "Error at Monday, 20 Nov 2023 08:24:40 +0000",
    "channel": "dialaxy-log",
    "attachments": [
        {
            "title": "Invalid Country code.",
            "color": "danger",
            "fields": [
                {"title": "Level", "value": None, "short": True},
                {"title": "Server Name", "value": "\n 127.0.0.1-local\n ", "short": True},
                {"title": "Method", "value": "POST", "short": True},
                {"title": "Path", "value": "/api/v1/contact/create/", "short": True},
                {"title": "User", "value": "Diwash Bhandari(mayahold@getnada.com)", "short": True},
                {"title": "Status Code", "value": None, "short": True},
                {"title": "Date", "value": "Mon Nov 20 08:24:40 2023", "short": True},
                {"title": "Agent", "value": "PostmanRuntime/7.35.0", "short": True},
            ],
        },
        {
            "color": "danger",
            "title": "Error Details",
            "text": None,
            "footer": "Invalid Country code.",
            "ts": 1700468680.3914886,
        },
    ],
}

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

response = requests.post(SLACK_WEBHOOK_URL, json=data)

print(response.text)
