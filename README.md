=====================================
Super Json Normalize (with Array Ultra)
=====================================


.. image:: https://img.shields.io/pypi/v/super_json_normalize.svg
        :target: https://pypi.python.org/pypi/super_json_normalize

.. image:: https://img.shields.io/travis/AdamRuddGH/super_json_normalize.svg
        :target: https://travis-ci.com/AdamRuddGH/super_json_normalize

.. image:: https://readthedocs.org/projects/super-json-normalize/badge/?version=latest
        :target: https://super-json-normalize.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/AdamRuddGH/super_json_normalize/shield.svg
     :target: https://pyup.io/repos/github/AdamRuddGH/super_json_normalize/
     :alt: Updates



A generic, unlimited level json normalizer which handles arrays at any location. Outputs a normalised set of data which can be imported into a relational table

## Why do I need this?

- This outputs relational data from pretty much and analytics focuse json
- It'll create new entities for data which should be split out into a new table
- It'll link those entries by a set list of ID keys you specify
- All your join keys are yours, so you won't get random breakages if you switch tools etc

If you're reporting within a relational Database, or have something in the pipeline which doesn't like structured data, this tool will do the heavy lifting to relationalise the json for you.
This will save you and your teams time doing the work of unnesting objects and pulling arrays into new tables so you can query them without the weird mappings that forced unnesting offers

* Free software: MIT license
* Documentation: https://super-json-normalize.readthedocs.io.

## How do i use it for my project?

This works well as a transform step for your ETL (or even ELT)
- Extract your data
- Iterate through each entry
- Run `super_json_normalize.normalize_record(<your_dict_here>)` on the entry
- pipe the output arrays of entries to your needed location 


Features
--------

* TODO
- initial dumb unnesting with `id` as the Primary key
- unnesting with configurable Primary Keys
- multiple Primary keys for parent
- multi-layerd primary keys (eg entities inside entities)

# Design

This works by pulling out arrays into their own entities. 

for the following example payload `properties` for a house (in directory /samples/property_data/):
```json
//for the file property_data.json
{
        "id": "ID001",
        "address": {
                "street_address": "123 Fake street",
                "suburb": "Fakeland",
                "state": "VIC",
                "country": "Australia"
        },
        "inspection_times": [
                {"id": "IID001", "description":"First inspection date on Sunday"},
                {"id": "IID002", "description":"Second inspection date on Tuesday"},
                {"id": "IID003", "description":"Final inpection date on Friday"}
        ]
        
}
```
The following will occur when we run `super_json_normalize.normalize_record()` on the loaded json data:
- the `address` object will be unnested
- a new entitiy called `inspection_times` will be created, and the `inspection_times` array will be removed from the root entity
- the parent `id` from the root will be pulled into the `inspection_times` entity so we can join the data

this would end up with:
```json

// `properties` entity
{ 
        "properties" : [
                {
                        "id": "ID001",
                        "address_street_address": "123 Fake street",
                        "address_suburb": "Fakeland",
                        "address_state": "VIC",
                        "address_country": "Australia"
                }
        ]
}

// `inspection_times` entity
{ 
        "properties_inspection_times": [
                {
                        "properties_id": "ID001",
                        "id": "IID001",
                        "description":"First inspection date on Sunday"
                },
                {
                        "properties_id": "ID001",
                        "id": "IID002",
                        "description":"Second inspection date on Tuesday"
                },
                {
                        "properties_id": "ID001",
                        "id": "IID003", 
                        "description":"Final inpection date on Friday"
                }
        ]
}

```

This is useful for preparing data for a relational db or systems requiring relational data.


# usage

example to dump each entity to json from the sample above

```python
import super_json_normalize as sjn 
import json

data = <your dict here eg with 1 array in it>
my_normalized_data = sjn.normalize(data) #returns list

print(my_normalized_data)

> [ {"properties": [ <each entry here>]}, {"properties_inspection_times": [ <each entry here>]} ]

for eachitem in my_normalized_data:
        with open(f"{eachitem.keys()}.json", "w") as json_file_to_write_to: #use the key of the dictionary as the name
                json.dump(eachitem, json_file_to_write_to)

```


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
