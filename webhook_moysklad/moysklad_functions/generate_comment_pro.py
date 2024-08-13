import base64
import json

import requests

from moysklad_comment_pro.get_customer_order_by_id import get_customer_order_by_id

# MoySklad credentials
username = 'admin@chainmetall'
password = 'Tashkent77'

# Encode credentials to base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()


def generate_comment_pro(customer_order_data, attribute_id="f6062d18-53bd-11ef-0a80-147e0006b1f8"):
    # Parse the JSON data
    # data = json.loads(customer_order_data)
    data = customer_order_data

    # Extract order ID
    customer_order_id = data["id"]

    # Load existing orders from the JSON file
    try:
        with open('orders.json', 'r') as json_file:
            orders_database = json.load(json_file)
    except FileNotFoundError:
        orders_database = {}

    # Initialize the list to collect position names for the text generation
    new_position_names_list = []

    # Check if the order already exists in the dictionary
    if customer_order_id in orders_database:
        # The order exists, find and store only new positions
        for position in data["positions"]["rows"]:
            position_id = position["id"]
            position_name = position["assortment"]["name"]

            # If the position is new, add it to the list for text generation
            if position_id not in orders_database[customer_order_id]:
                new_position_names_list.append(f"{position_name} --\n")

            # Update or add the position in the order
            orders_database[customer_order_id][position_id] = {"name": position_name}
    else:
        # The order is new, store all positions
        orders_database[customer_order_id] = {}
        for position in data["positions"]["rows"]:
            position_id = position["id"]
            position_name = position["assortment"]["name"]

            # Add all positions to the list for text generation
            new_position_names_list.append(f"{position_name} --\n")

            # Store the position in the order
            orders_database[customer_order_id][position_id] = {"name": position_name}

    # Check for the specific attribute in "attributes"
    attribute_value = None

    for attribute in data.get("attributes", []):
        if attribute["id"] == attribute_id:
            attribute_value = attribute["value"]
            break

    # Generate the text for the attribute
    if new_position_names_list:
        new_positions_text = "".join(new_position_names_list)

        if attribute_value:
            # Update the existing attribute value with new positions
            updated_attribute_value = f"{attribute_value} \n {new_positions_text}"
            print(f"Updated attribute value: {updated_attribute_value}")
        else:
            # Create a new attribute value if it doesn't exist
            updated_attribute_value = new_positions_text
            print(f"Created new attribute value: {updated_attribute_value}")

        # Prepare the body for the PUT request
        payload = {
            "attributes": [
                {
                    "meta": {
                        "href": f"https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/{attribute_id}",
                        "type": "attributemetadata",
                        "mediaType": "application/json"
                    },
                    "value": updated_attribute_value
                }
            ]
        }

        # Perform the PUT request to update the attribute
        url = f"https://api.moysklad.ru/api/remap/1.2/entity/customerorder/{customer_order_id}"
        headers = {
            "Authorization": f'Basic {credentials}',  # Replace with your token
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("Order attribute updated successfully. Response: ", response.json())
        else:
            print(f"Failed to update order attribute: {response.status_code} - {response.text}")
    else:
        print("No new positions found.")

    # Save the updated orders dictionary back to the JSON file
    with open('orders.json', 'w') as json_file:
        json.dump(orders_database, json_file, indent=4)

    print("Data updated and saved to orders.json.")


if __name__ == '__main__':
    order_id = '09ef1013-5933-11ef-0a80-18420001f3aa'
    generate_comment_pro(get_customer_order_by_id(order_id))
