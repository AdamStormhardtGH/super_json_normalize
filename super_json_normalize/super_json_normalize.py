"""Main module."""

import json


def load_json(json_path):
    """safely load json file from location"""
    with open(json_path,"r") as jsf:
        return json.load(jsf)

def merge_two_dicts(dict_01, dict_02):
    """ for python 3.4 or lower """
    merged_dict = dict_01.copy()   # start with x's keys and values
    merged_dict.update(dict_02)    # modifies z with y's keys and values & returns None
    return merged_dict

def scan_layer0(json_object):
    """ scans the first layer of the json, flagging arrays """

    arrays = []
    dicts = []
    flattend_dict = {}
    for key, value in json_object.items():
        if isinstance(value, dict):
            flattend_dict = merge_two_dicts(flattend_dict,flatten_object(key,value))
        elif isinstance(value, list):
            arrays.append({key: value})
        else:
            flattend_dict[key] = value
    
    #flatten arrays

    print("Arrays:")
    print(arrays)

    flattened_array = []
    for each_array in arrays:
        for each_permutation in each_array:
            print(f"Permutatoin of array {each_permutation}")
            flattened_array.append(merge_two_dicts(each_permutation,flattend_dict)  )
        
    return(flattend_dict)

def flatten_object(object_key,object_contents, delimeter="_"):
    """ will flatten dicts"""
    new_object = {  }
    for dict_key, dict_value in object_contents.items():
        new_key = f"{object_key}_{dict_key}"
        new_object[new_key]= dict_value
    
    return(new_object)

def flatten_array(array_key, array_contents, delimeter="_"):
    """ will flaten arrays """
    output_array = []
    for each_item in array_contents:
        if isinstance(each_item, dict):
            print(each_item)
            output_array.append(flatten_object(array_key,each_item) )
        #not supporting non object data in arrays for now
    return output_array

my_json = {"hello":"sailor", "my":{"name":"wife"}, "arrayhere":[ {"contents01":"something"}, {"contents01":"else"} ]}

print(scan_layer0(my_json) )
# print(flatten_array("butts",my_json["arrayhere"]))


# my_big_json = load_json("input_files/genesys_example.json")
# print(scan_layer0(my_big_json) )

