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


# Design

This works in layers. It needs to understand which layer we're on, so when we explode out arrays, they're applied to the appropriate location. This will create a lot of duplication, but it will flatten any shape

layer 0: 
- apply root analysis on type. flag sections which will need to be expanded on. 
layer 1 arrays:
- apply root analysis on type. flag sections which need to be expanded on and relationalise 
- fold back into dataset, applying each array incrementally
- layer 1 has now been collapsed and is now layer 0.
- repeat until no arrays found
- return resulting set of data


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
