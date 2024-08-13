import base64
import requests

# MoySklad credentials
username = 'admin@chainmetall'
password = 'Tashkent77'

# Encode credentials to base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()


def get_customer_order_by_id(order_id):
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-type': 'application/json'
    }

    # Add the expand query parameters to the URL
    url = f'https://api.moysklad.ru/api/remap/1.2/entity/customerorder/{order_id}?expand=positions.assortment,attributes'

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        print(f'Order of id data: {data}')
        return data
    else:
        print(f'Failed get order by ID: {order_id}')
        print(f'Status code: {response.status_code}')
        print(f'Error: {response.text}')
        return ''
