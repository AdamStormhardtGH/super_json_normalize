=====================================
Super Json Normalize with Array Ultra
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


* Free software: MIT license
* Documentation: https://super-json-normalize.readthedocs.io.


Features
--------

* TODO
- initial dumb unnesting with `id` as the Primary key
- unnesting with configurable Primary Keys
- multiple Primary keys for parent
- multi-layerd primary keys (eg entities inside entities)

# Design

This works by pulling out arrays into their own entities. 

for the following example payload `properties` for a house:
```json
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
The following will occur:
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
