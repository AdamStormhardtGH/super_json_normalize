"""Main module."""

import json
import copy


def load_json(json_path):
    """safely load json file from location"""
    with open(json_path,"r") as jsf:
        return json.load(jsf)

def merge_two_dicts(dict_01, dict_02):
    """ for python 3.4 or lower """
    print(f"merging {dict_01} and {dict_02}")
    merged_dict = dict_01.copy()   # start with x's keys and values
    merged_dict.update(dict_02)    # modifies z with y's keys and values & returns None
    return merged_dict


def flatten_object(object_key,object_contents, delimeter="_"):
    """
    This function is designed to flatten dictionaries and identify new arrays. 
    it will return a dictionary with 2 aspects:
    - the flattened dict contents from the layer/s
    - arrays it will not approach

    note that this will recursively flatten

    returns: {"dictionary": {<dict_data>}, "array": [{<array key>:<array value},{<array key>:<array value}] }
    """
    output_dictionary = {}
    output_array = []
    flattened_dictionary = {}

    for dict_key, dict_value in object_contents.items():

        if isinstance(dict_value, (dict)):
            #if a list, call this recusively
            instance_output = flatten_object(object_key=dict_key, object_contents=dict_value)
            instance_dictionary = instance_output["dictionary"]
            instance_array = instance_output["array"]
            if len(instance_array) >0:
                output_array.extend(instance_array)
            output_dictionary = merge_two_dicts(output_dictionary,instance_dictionary) #join the dict

        elif isinstance(dict_value, list):
            #if the item is an array, we push it back to get processed elsewhere
            array_information = {"name": dict_key, "data": dict_value}
            output_array.append(array_information)
        
        else:
            #for the rest of the types of data
            new_dict_key = f"{object_key}_{dict_key}"
            flattened_dictionary[new_dict_key]= dict_value
    
    #finally, merge the dictionary so we can pull in all that recursive stuff
    output_dictionary = merge_two_dicts(output_dictionary,flattened_dictionary)
    
    #return the recursively flattened data, and the arrays we pulled out 
    #TODO: ensure the recursive arrays have paths to their locations
    #TODO: should remember the json_path imo
    return {"dictionary": output_dictionary, "array": output_array}

def flatten_array(array_key, array_contents, delimeter="_"):
    """ will flaten arrays """
    output_array = []
    for each_item in array_contents:
        if isinstance(each_item, dict):
            print(each_item)
            output_array.append(flatten_object(array_key,each_item) )
        #not supporting non object data in arrays for now
    return output_array

# def process_arrays(input_array):
#     """
#     Process the contents of an array. This mostly just cleans up the normalize_layer function
#     """
#     for each_entry in input_array:
#         normalize_layer(each_entry)

def normalize_layer(input_object, parent_name="default_name"):
    """ scans the first layer of the json, flagging arrays """

    arrays = []
    dicts = [] #only ever returns dicts
    # flattend_dict = {}


    output_dictionary = {}
    output_array = []
    # flattened_dictionary = {}
    
    #for each item in the object:
    # if the item is a non object or non list item: 
    # append to this flattened_dict object
    # if the item is a dictionary: 
    # trigger the flatten dict function
    # the flatten dict function will iterate through the items and append them to a dictionary. it will return a dictionary with {"dictionary": <dict_data>, "array": <arrays>}
        # join flattened_dict and the returned[dictionary] data
        # append returned[array] to arrays layer
    
    #arrays will be dealt with a little differently. Because we're expecting multiple entries we'll be workign with a loop which will always belong to an array
    # create new dict object dict_object = {"name": <dict name>, "data": [dict array entries data]}
    # for each in the array loop - trigger normalize_layer with parent name of array name
    # dict_object.append the `dicts_array`["data"] to the dict_object["data"] array

    if isinstance(input_object, (dict)):
        for key, value in input_object.items():
            if not isinstance(value, (dict,list) ):
                # if the item is a non object or non list item: 
                output_dictionary[key] = value

            elif isinstance(value, dict):
                # if the item is a dictionary: 
                # trigger the flatten dict function
                
                dict_contents = flatten_object(key,value) # will return {"dictionary": <dict_data>, "array": <arrays>}
                instance_dictionary = dict_contents["dictionary"]
                instance_array = dict_contents["array"]

                if len(instance_array) >0:
                    output_array.extend(instance_array)
                output_dictionary = merge_two_dicts(output_dictionary,instance_dictionary) #join the dict
                
            elif isinstance(value, list):
                arrays.append({"name":key, "data":value})

    elif isinstance(input_object, (list)):
        output_array.append({"name":parent_name,"data":input_object})

    
    print("Now we deal with Arrays:")
    
        # print(arrays)

        # flattened_array = []
    for each_array in arrays:
        array_instance = [] #because we're expecting 1+ entries we need to add to an array then pull it together
        print(each_array)
        for each_entry in each_array["data"]:
            normalized_array = (normalize_layer(input_object = each_entry, parent_name = each_array["name"]) ) 
            #expect list here
            #let the normalizer recursively work through and pull the data out. Once it's out, we can append the data to the dicts array :)
            #may return 1 or more dictionaries

            for each_normalized_array_entry in normalized_array:
                # iterate through each output in the normalized array

                #check if there is an instance of this data already
                matches = False
                for each_dictionary_entity in dicts:
                    if each_normalized_array_entry["name"] == each_dictionary_entity["name"]:
                        #check if there is data in place already for this. If so, we add an entry to it
                        each_dictionary_entity["data"].extend(each_normalized_array_entry["data"])
                        matches = True
                if matches == False:
                    # print(f"instance of processing: {each_normalized_array_entry}\n\n")
                    print("found no match! adding new table entry")
                    dicts.append({"name": each_normalized_array_entry["name"] , "data": each_normalized_array_entry["data"] })

            # if isinstance(each_array,list):
            #     for each_permutation in each_array:
            #         print(f"Permutation of array {each_permutation}")
            #         flattened_array.append(merge_two_dicts(each_permutation,flattend_dict)  )
            # else:
            #     flattened_array.append(merge_two_dicts(each_array,flattend_dict)  )

        # output_arrays = []

        # dict_name = parent_name 
        # layer_flattened_dict = {}
        # for key, value in input_object.items():
        #     if isinstance(value, dict):
        #         #if dictionary, we want to normalize the contents
        #         #run this normalize function recursively
        #         # flattend_dict = merge_two_dicts(flattend_dict,flatten_object(key,value))
        #         dict_contents = normalize(input_object = value, parent_name=key)
        #     elif isinstance(value, list):
        #         pass
        #     else:
        #         layer_flattened_dict[f"{parent_name}_{key}"] = value
        # dict_object_for_
        # output_arrays.append()
    
    dicts.append({"name":parent_name, "data": [output_dictionary]})
        
    return(dicts)

my_json = {"hello":"sailor", "my":{"name":"wife"}, "arrayhere":[ {"contents01": {"more":"something", "more2":"somethingmre"}, "contents02":"else" },{"hey":"00","contents02":"else"} ]}


# start again

print(json.dumps(normalize_layer(my_json), indent=2 ))

# print(json.dumps(flatten_object("boobs",my_json), indent=2 ) )

#pass to flatten and split - taking name of doc
# returns arrays only ["dict_name":{<data>}]

