"""Main module."""

import json
from logging import error

def clean_path(directory_path) -> str:
    """
    Will ensure the path supplied DOES end with / so we can join to a filename without worry
    """
    

    if str(directory_path):
        if directory_path[-1:] != "/":
            directory_path = directory_path + "/"
    return directory_path


def load_json(json_path):
    """
    Safely load json file from a path location
    eg. open("./json_files/my_json_file.json")
    """

    with open(json_path,"r") as jsf:
        return json.load(jsf)

def write_json(data, file_name, file_path=".", append=False):
    """
    Safely write to a json file in a path
    - data = the dictionary data you want to write
    - file_name = the file name you indend to write to
    - file_path = the path you want to write to
    - append = add to the file 
    """
    
    
    if append:
        write_mode = "wa"
    else:
        write_mode = "w"

    clean_file_path = clean_path(file_path) #clean the path

    with open(f"{clean_file_path}{file_name}.json", write_mode) as jsf:
        json.dump(data, jsf)



def write_jsonl(data, file_name, file_path=".", append=False):
    """
    safely write to a json file in line delimited json format
    """


    if append:
        write_mode = "wa"
    else:
        write_mode = "w"

    jsonl_contents = ""
    for each_entry in data:
        jsonl_contents = jsonl_contents + "\n" + json.dumps(each_entry)

    clean_file_path = clean_path(file_path) #clean the path

    with open(f"{clean_file_path}{file_name}.jsonl", write_mode) as jsf:
        jsf.write(jsonl_contents)



def merge_two_dicts(dict_01, dict_02):
    """ 
    Merge 2 dictionaries and return the merged dictionary. 
    Compatible with python 3.4 or lower
    """
    
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


def extract_parent_keys(dictionary_name, dictionary_object,list_of_ids_to_include=["id"]):
    """
    Returns a list of ids from an object which match a list of strings
    This is a simple implementation which needs to be improved upon, but should cover the basics of joins
    """


    items_to_return = {}
    if not isinstance(dictionary_object, dict):
        return {}
    else:
        for each_dict_item in dictionary_object.keys():
            #look through each item in the dict. We need to look to see if our keywords are in these keys and return the keys as a dict we can insert 
            for each_flagged_item in list_of_ids_to_include:
                if str(each_flagged_item).lower() in str(each_dict_item).lower():
                    dict_item = {f"{dictionary_name}_{each_dict_item}": dictionary_object[each_dict_item] }
                    items_to_return = merge_two_dicts(items_to_return,dict_item)
    return items_to_return

def normalize_record(input_object, parent_name="root_entity"):
    """ 
    This function orchestrates the main normalization. 
    It will go through the json document and recursively work with the data to:
    - unnest (flatten/normalize) keys in objects with the standard <parentkey>_<itemkey> convention
    - identify arrays, which will be pulled out and normalized
    - create an array of entities, ready for streaming or export 
    
        for each item in the object:
        if the item is a non object or non list item: 
        append to this flattened_dict object
        if the item is a dictionary: 
        trigger the flatten dict function
        the flatten dict function will iterate through the items and append them to a dictionary. it will return a dictionary with {"dictionary": <dict_data>, "array": <arrays>}
            join flattened_dict and the returned[dictionary] data
            append returned[array] to arrays layer
        
        arrays will be dealt with a little differently. Because we're expecting multiple entries we'll be workign with a loop which will always belong to an array
        create new dict object dict_object = {"name": <dict name>, "data": [dict array entries data]}
        for each in the array loop - trigger normalize_layer with parent name of array name
        dict_object.append the `dicts_array`["data"] to the dict_object["data"] array
    
    """


    arrays = []
    dicts = []
    output_dictionary = {}

    parent_keys = extract_parent_keys(dictionary_name=parent_name, dictionary_object=input_object)

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
                    arrays.extend(instance_array)
                output_dictionary = merge_two_dicts(output_dictionary,instance_dictionary) #join the dict
                
            elif isinstance(value, list):
                arrays.append({"name":key, "data":value, "parent_keys": parent_keys})

    elif isinstance(input_object, (list)):
        arrays.append({"name":parent_name,"data":input_object })

    ##############################
    ### Now process the arrays ###
    ##############################
    

    for each_array in arrays:
        for each_entry in each_array["data"]:
            each_entry = each_entry
            try:
                if each_array["parent_keys"]:
                    each_entry = merge_two_dicts(each_entry, each_array["parent_keys"])
            except:
                pass

            normalized_array = (normalize_record(input_object = each_entry, parent_name = each_array["name"]) ) 
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
                    dicts.append({"name": each_normalized_array_entry["name"] , "data": each_normalized_array_entry["data"] })

          
    dicts.append({"name":parent_name, "data": [output_dictionary]})
        
    return(dicts)


def export_records(normalized_records, path="./export_data", format="json"):
    """
    Will save out the records into the specified path in the format 
    formats:
    - "json" standard json format. outputs as array
    - "jsonl" line delimited json. Each row is an object. This is used in spark etc and big data
    TODO: CSV / TSV
    """


    if not isinstance(normalized_records, list):
        raise error("No records to export - normalized records are not a list type. Something has gone wrong with the generation, or the generation has not happened yet")
    else:
        for eachrecord in normalized_records:
                if format == "json":
                    write_json(eachrecord["data"],eachrecord["name"],file_path=path)
                elif format == "jsonl":
                    write_jsonl(eachrecord["data"],eachrecord["name"],file_path=path)
            
                


# my_sample_data = load_json("samples/property_data/property_data.json")

# my_output_data = normalize_record(my_sample_data, parent_name="properties")

# # print(json.dumps(my_output_data, indent=2))

# export_records(my_output_data, format="jsonl")


# print(clean_path("hello/") )