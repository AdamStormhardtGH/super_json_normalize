"""
This is an example file showing basic use of the Super Json Normalize package
"""
import json
from ...super_json_normalize import super_json_normalize as sjn

my_sample_data = sjn.load_json("./property_data.json")

my_output_data = sjn.normalize_layer(my_sample_data)

print(json.dumps(my_output_data, indent=2))