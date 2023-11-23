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

SLACK_SUBSCRIPTION_WEBHOOK_URL = ""


async def send_message(message):
    subscription_webhook = SLACK_SUBSCRIPTION_WEBHOOK_URL
    headers = {"Content-type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            subscription_webhook, json=message, headers=headers
        )
        print(response.status_code)
        print(response.text)


# asyncio.run(send_message(message))


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
print(message)
