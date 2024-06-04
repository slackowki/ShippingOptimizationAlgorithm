import pandas as pd
from get_shipping_rate import load_address_data, get_shipping_rate

from_address_data = load_address_data('JSON Info/shipping_from.json')["SHIPPING_FROM"]
to_address_data = load_address_data('JSON Info/shipping_to.json')["EXAMPLE_ADDRESS_1"]

product_dimensions_data = load_address_data('JSON Info/product.json')["dimensions"]

def generate_combinations(base_value, min_value, min_offset, max_offset, step):
    return [base_value + offset for offset in range(min_offset, max_offset + step, step) if base_value + offset >= min_value]

def test_combinations():
    base_weight = product_dimensions_data["weight"]["value"]
    base_length = product_dimensions_data["length"]["value"]
    base_width = product_dimensions_data["width"]["value"]
    base_height = product_dimensions_data["height"]["value"]
    
    min_weight = product_dimensions_data["weight"]["min_value"]
    min_length = product_dimensions_data["length"]["min_value"]
    min_width = product_dimensions_data["width"]["min_value"]
    min_height = product_dimensions_data["height"]["min_value"]
    
    weight_combinations = generate_combinations(base_weight, min_weight, -2, 2, 2)
    length_combinations = generate_combinations(base_length, min_length, -6, 6, 6)
    width_combinations = generate_combinations(base_width, min_width, -6, 6, 6)
    height_combinations = generate_combinations(base_height, min_height, -6, 6, 6)
    
    loop_data = []

    loop_counter = 1
    lowest_cost = None
    best_dimensions = None

    for weight in weight_combinations:
        for length in length_combinations:
            for width in width_combinations:
                for height in height_combinations:
                    product_data = {
                        "weight": {"value": weight},
                        "weight_unit": product_dimensions_data["weight_unit"],
                        "dimension_unit": product_dimensions_data["dimension_unit"],
                        "length": {"value": length},
                        "width": {"value": width},
                        "height": {"value": height}
                    }
                    shipping_cost = get_shipping_rate(product_data, from_address_data, to_address_data)
                    print(f"Shipment Loop {loop_counter}:")
                    print(f"Weight={weight} lb") 
                    print(f"Length={length} in") 
                    print(f"Width={width} in") 
                    print(f"Height={height} in") 
                    print(f"Shipping Cost={shipping_cost}")

                    loop_info = {
                        "Shipment Loop": loop_counter,
                        "Weight": weight,
                        "Length": length,
                        "Width": width,
                        "Height": height,
                        "Shipping Cost": shipping_cost
                    }
                    loop_data.append(loop_info)

                    if shipping_cost is not None:
                        if lowest_cost is None or shipping_cost < lowest_cost:
                            lowest_cost = shipping_cost
                            best_dimensions = {
                                "weight": weight,
                                "length": length,
                                "width": width,
                                "height": height
                            }

                    loop_counter += 1

    if lowest_cost is not None:
        print(f"Lowest Shipping Cost: {lowest_cost}")
        print(f"Best Dimensions:")
        print(f"Weight={best_dimensions['weight']} lb")
        print(f"Length={best_dimensions['length']} in")
        print(f"Width={best_dimensions['width']} in")
        print(f"Height={best_dimensions['height']} in")
    else:
        print("No valid shipping costs were found.")

    df = pd.DataFrame(loop_data)
    
    df.to_csv('shipment_quotes.csv', index=False)

test_combinations()