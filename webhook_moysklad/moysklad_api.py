import requests

import barcode

import base64
from io import BytesIO

from barcode.writer import ImageWriter

from datetime import datetime, timedelta

# MoySklad credentials
username = 'admin@chainmetall'
password = 'Tashkent77'
check_number_id = '87313ddd-4bee-11ef-0a80-072c00359ce7'
barcode_id = '1ca64e44-4d03-11ef-0a80-00d000455387'

# Encode credentials to base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
today_date = datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')


def get_barcode_base64(order_name):
    barcode_class = barcode.get_barcode_class('code128')

    options = {
        'module_width': 0.2,   # width of one barcode module (default is 0.2)
        'module_height': 7.0, # height of the barcode (default is 15.0)
        'quiet_zone': 0.7,     # space on left and right side of barcode (default is 6.5)
        'font_size': 6,       # size of the text under the barcode (default is 10)
        'text_distance': 3.0,  # distance between barcode and text (default is 5.0)
        'write_text': True,    # whether to write the text under the barcode (default is True)
        'background': 'white', # background color (default is 'white')
        'foreground': 'black', # foreground (bar) color (default is 'black')
        'dpi': 300,            # resolution of the image (default is 300)
    }

    my_barcode = barcode_class(order_name, writer=ImageWriter())
    buffer = BytesIO()
    my_barcode.write(buffer, options)
    buffer.seek(0)

    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return base64_image


def get_customer_order_by_id(order_id):
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-type': 'application/json'
    }

    url = f'https://api.moysklad.ru/api/remap/1.2/entity/customerorder/{order_id}'

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        print(f'Order of id data: {data}')
        return data
    else:
        print(f'Failed get order by ID: {order_id}')
        print(f'Status code: {response.status_code}')
        print(f'Error: {response.text}')


def get_customer_orders_size():
    # Set the headers
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }

    # URL for deleting the webhook
    url = f"https://api.moysklad.ru/api/remap/1.2/entity/customerorder"

    params = {
        'filter': f'moment>={yesterday} 23:00:00.000'
    }

    # Make the request
    response = requests.get(url, headers=headers, params=params)
    size = response.json()['meta']['size']

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Customer orders: {size}")
        return size
    else:
        print(f"Failed to get customer orders. Status code: {response.status_code}, Response: {response.text}")
        return response.status_code


def update_customer_order_check_number_by_id(order_id, size):
    data = get_customer_order_by_id(order_id)
    base64_image = get_barcode_base64(data['name'])

    # order_number = data['name']

    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }

    payload = {
        
        'attributes': [
            {
                'meta': {
                    'href': f'https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/{check_number_id}',
                    'type': 'attributemetadata',
                    'mediaType': 'application/json'
                },
                'value': size
            },
            # Barcode
            {
                'meta': {
                    'href': f'https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/{barcode_id}',
                    'type': 'attributemetadata',
                    'mediaType': 'application/json'
                },
                'file': {
                    "filename":"barcode.png",
                    "content":base64_image
                }
            }
        ],

    }

    # URL for deleting the webhook
    url = f"https://api.moysklad.ru/api/remap/1.2/entity/customerorder/{order_id}"

    # Make the request
    response = requests.put(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Updated customerOrder: {response.json()['name']}")
    else:
        print(f"Failed to update customer order. Status code: {response.status_code}, \nResponse: {response.text}")


if __name__ == '__main__':
    get_customer_orders_size()
