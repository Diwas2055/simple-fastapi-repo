import asyncio
import httpx


message = {
    "text": "Number Reserved Notification",
    "attachments": [
        {
            "color": "#36a64f",
            "title": "Number Reservation Information",
            "fields": [
                {"title": "Reserved Number", "value": "+12185142299", "short": True},
                {
                    "title": "Reserved By",
                    "value": "Diwash Bhandari(mayahold@getnada.com)",
                    "short": True,
                },
            ],
            "footer": "Number Reserved Notification | Nov 14, 2023",
        }
    ],
}


from datetime import datetime
from faker import Faker

fake = Faker()

# Example payload with fake data
payload = {
    "plan_type": "Gold",
    "time_info": "1 month",
    "full_name": fake.name(),
    "email": fake.email(),
    "amount": fake.random_int(min=50, max=200),
    "renew_date": fake.future_date(),
    "str_date": fake.date_time_this_decade(),
}

text = "Subscription Success Notification"
message = {
    "text": f"{text}",
    "attachments": [
        {
            "color": "#439FE0",
            "title": "Subscription Details",
            "fields": [
                {
                    "title": "Plan",
                    "value": f"{payload['plan_type']} | {payload['time_info']}",
                    "short": True,
                },
                {
                    "title": "Subscriber",
                    "value": f"{payload['full_name']}({payload['email']})",
                    "short": True,
                },
                {
                    "title": "Amount",
                    "value": f"${payload['amount']}",
                    "short": True,
                },
                {
                    "title": "Renew Date",
                    "value": f"{payload['renew_date']}",
                    "short": True,
                },
            ],
            "footer": f"{text} | {payload['str_date']}",
        }
    ],
}

# Print the generated message
# print(message)


payload = {
    "reserved_number": fake.random_number(digits=8),
    "provider_name": fake.company(),
    "country_name": fake.country(),
    "code": fake.random_int(min=100, max=999),
    "full_name": fake.name(),
    "email": fake.email(),
    "str_date": fake.date_time_this_decade(),
}

text = "Number Reserved Notification"
message = {
    "text": f"{text}",
    "attachments": [
        {
            "color": "#36a64f",
            "title": "Number Reservation Information",
            "fields": [
                {
                    "title": "Reserved Number",
                    "value": f"{payload['reserved_number']}",
                    "short": True,
                },
                {
                    "title": "Provider",
                    "value": f"{payload['provider_name'].capitalize()}",
                    "short": True,
                },
                {
                    "title": "Country",
                    "value": f"{payload['country_name']} ({payload['code']})",
                    "short": True,
                },
                {
                    "title": "Reserved By",
                    "value": f"{payload['full_name']}({payload['email']})",
                    "short": True,
                },
            ],
            "footer": f"{text} | {payload['str_date']}",
        }
    ],
}

# Print the generated message
# print(message)


message_error = {
    "channel": "dialaxy-log",
    "attachments": [
        {
            "title": "ZeroDivisionError",
            "color": "danger",
            "fields": [
                {"title": "Level", "value": "ERROR", "short": True},
                {
                    "title": "Server Name",
                    "value": "\n                        127.0.0.1-local\n                        ",
                    "short": True,
                },
                {"title": "Method", "value": "GET", "short": True},
                {"title": "Path", "value": "/api/v1/countries/", "short": True},
                {
                    "title": "User",
                    "value": "Diwash Bhandari(mayahold@getnada.com)",
                    "short": True,
                },
                {"title": "Status Code", "value": 500, "short": True},
                {"title": "Date", "value": "Fri Nov 24 02:56:21 2023", "short": True},
                {
                    "title": "User Agent",
                    "value": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                    "short": True,
                },
            ],
        },
        {
            "color": "danger",
            "title": "Error Details",
            "text": "division by zero",
            "footer": "ZeroDivisionError",
            "ts": 1700794581.8972974,
        },
    ],
}


SLACK_WEBHOOK_URL = ""


async def send_message(message):
    subscription_webhook = SLACK_WEBHOOK_URL
    headers = {"Content-type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            subscription_webhook, json=message, headers=headers
        )
        print(response.status_code)
        print(response.text)


asyncio.run(send_message(message_error))
