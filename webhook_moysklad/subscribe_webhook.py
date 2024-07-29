import requests
import base64

# MoySklad credentials
username = 'admin@chainmetall'
password = 'Tashkent77'

# Encode credentials to base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()


def delete_webhook(webhook_id):
    # Set the headers
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }

    # URL for deleting the webhook
    url = f"https://api.moysklad.ru/api/remap/1.2/entity/webhook/{webhook_id}"

    # Make the request
    response = requests.delete(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Webhook with ID {webhook_id} deleted successfully.")
    else:
        print(f"Failed to delete webhook. Status code: {response.status_code}, Response: {response.text}")


def get_hooks():
    # API URL
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/webhook'

    # Headers
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }

    # Send GET request to retrieve webhooks
    response = requests.get(url, headers=headers)

    # Print response
    if response.status_code == 200:
        webhooks = response.json()
        print(webhooks)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def subscribe():
    # API URL
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/webhook'

    # Webhook data
    webhook_data = {
        "url": "https://crmhelper.uz/",
        "action": "CREATE",
        "entityType": "customerorder"  # Change to the appropriate entity type
    }

    # Headers
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }

    # Send POST request to create webhook
    response = requests.post(url, json=webhook_data, headers=headers)

    # Print response
    print(response.status_code)
    print(response.json())


if __name__ == '__main__':
    subscribe()
    # get_hooks()
    # delete_webhook("43ec58c7-4c69-11ef-0a80-086a00964dda")
