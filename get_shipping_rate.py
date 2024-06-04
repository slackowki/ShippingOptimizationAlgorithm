import requests
import json

def load_address_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_shipping_rate(product_data, from_address_data, to_address_data):
    url = "https://api.shipengine.com/v1/labels"

    payload = {
        "shipment": {
            "packages": [
                {
                    "weight": {
                        "value": product_data["weight"]["value"],
                        "unit": product_data["weight_unit"]["value"]
                    },
                    "dimensions": {
                        "unit": product_data["dimension_unit"]["value"],
                        "length": product_data["length"]["value"],
                        "width": product_data["width"]["value"],
                        "height": product_data["height"]["value"]
                    }
                }
            ],
            "service_code": "ups_ground",
            "ship_to": {
                "name": to_address_data["name"],
                "phone": to_address_data["phone"],
                "address_line1": to_address_data["street1"],
                "city_locality": to_address_data["city"],
                "state_province": to_address_data["state"],
                "postal_code": to_address_data["zip"],
                "country_code": to_address_data["country"],
                "address_residential_indicator": "yes"
            },
            "ship_from": {
                "company_name": from_address_data["company"],
                "name": from_address_data["name"],
                "phone": from_address_data["phone"],
                "address_line1": from_address_data["street1"],
                "address_line2": from_address_data.get("street2", ""),
                "city_locality": from_address_data["city"],
                "state_province": from_address_data["state"],
                "postal_code": from_address_data["zip"],
                "country_code": from_address_data["country"],
                "address_residential_indicator": "no"
            }
        }
    }

    with open('Json Info/api_key.json', 'r') as f:
        api_info = json.load(f)
        api_key = api_info['api_key']

    headers = {
        'Host': 'api.shipengine.com',
        'API-Key': api_key,  # Replace with your ShipEngine API key
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            shipment_cost = response_data.get("shipment_cost", {})
            if shipment_cost:
                rate_amount = shipment_cost.get("amount")
                if rate_amount is not None:
                    print(rate_amount)
                    return rate_amount
                else:
                    print("No rate amount found.")
                    return None
            else:
                print("No shipment cost found in response.")
                return None
        else:
            print(f"Failed to create label. Status code: {response.status_code}, Error message: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to send request. Error: {e}")
        return None

from_address_data = load_address_data('JSON Info/shipping_from.json')["SHIPPING_FROM"]
to_address_data = load_address_data('JSON Info/shipping_to.json')["EXAMPLE_ADDRESS_1"]
product_dimensions_data = load_address_data('Json Info/product.json')["dimensions"]

product_data = {
    "weight": product_dimensions_data["weight"],
    "weight_unit": product_dimensions_data["weight_unit"],
    "dimension_unit": product_dimensions_data["dimension_unit"],
    "length": product_dimensions_data["length"],
    "width": product_dimensions_data["width"],
    "height": product_dimensions_data["height"]
}


