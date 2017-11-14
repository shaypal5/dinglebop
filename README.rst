dinglebop
#########
|PyPI-Status| |PyPI-Versions| |Build-Status| |Codecov| |LICENCE|

Automate and version dataset storage and caching.

.. code-block:: python

  import dinglebop
  # mystery code

.. contents::

.. section-numbering::


Installation
============

.. code-block:: bash

  pip install dinglebop


Getting started
===============

Architecture
------------

To use ``dinglebop`` to store and version your datasets you must set up an instance of the system, called a dingle. There are two types of dingles:

* A standard dingle is composed of a single index, one or more stores and zero or more caches.
* A consolidated dingle is composed of a single index-store server and zero or more caches. 

Once set up, a request to load a dataset stored in this dingle checks first for a machine-local copy of the requested dataset and version, and then goes on to query caches, finally backing off to check against the index which store should the dataset be loaded from.

Additionally, having an index over versioned datasets enables fuzzier requests like getting the latest version of a dataset, or any version satisftying some set of constaints, and other such queries. 

The configuration file
----------------------

``dinglebop`` can be easilly configured by editing its configuration file. First, if it doesn't already exists, create a ``.dinglebop`` folder under your home folder, and inside it create a json file named ``dinglebop_cfg.json``.

The configuration file should adhere to the following structure:

.. code-block:: json
    
    {
        "dingles": {
            "production_dingle": {
                # dingle configuration...
            },
            "research_dingle": {
                # dingle configuration...
            }
        }
    }

The inner structure for each dingle depdends on its type.

Standard dingle configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As mentioned, a standard dingle is composed of a single index, one or more stores and zero or more caches. As such, the corresponding dingle configuration object reflects the same structure:

.. code-block:: json

    ...
    "production_dingle": {
        "index": {
            # inner index configuration...
        },
        "stores": [
            {
                "name": "s3_prod_ds_store",
                # inner store configuration...
            }
        ],
        "caches": [
            {
                "name": "redis_prod_ds_cache",
                # inner cache configuration...
            }
        ]
    }

The order in which different store and cache entries are given determines the preference order among them. The specifics of the configuration of each index, store or cache depends on its type, and is given in the documentation of that type. For example, a MongoDB-based dingle index might require you to supply values for fields such as hostnames, username, password and collection name inside the index configuration object.

Consolidated dingle configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A consolidated dingle is composed of a single index-store server and zero or more caches. The configuration of such a dingle reflects the same structure:

.. code-block:: json

    ...
    "research_dingle": {
        "index-store": {
            # inner index-store configuration...
        },
        "caches": [
            {
                "name": "redis_prod_ds_cache",
                # inner cache configuration...
            }
        ]
    }

The order in which different cache entries are given determines the preference order among them. The specifics of the configuration of each index-store or cache depends on its type, and is given in the documentation of that type. 


Basic Use
=========

``pass``


Possible Components
===================

Indexes
-------

Indexes are used by a dingle to track all the different datasets stored in it, as well as their different versions.

MongoDB-based index
~~~~~~~~~~~~~~~~~~~

A MongoDB-based index uses a single collection on a MongoDB server to index datasets. As such, you need to create a dedicated collection on a MongoDB server (any required indexes will be created automatically) and supply ``dinglebop`` with the following parameters inside the index configuration object:

* ``type`` - Must be given the value ``MongoDB``.
* ``hosts`` - A list of host address strings of the form ``<hostname>:<port>``.
* ``username`` - A user name used for authentication. The corresponding user must have writing permissions for the provided collection.
* ``password`` - A password used for authentication.
* ``db_name`` - The name of the database which contains the index collection on the target server.
* ``collection_name`` - The name of the collection which contains the index on the target server.

Any additional keyword arguments are supplied to the constructor of ``pymongo.mongo_client.MongoClient`` (see `pymongo's documentation <http://api.mongodb.com/python/current/api/pymongo/mongo_client.html?highlight=mongo_client#module-pymongo.mongo_client>`_ for a list of possible parameters). 

For example, if users for the given database reside on the database itself (and not on the ``admin`` database of the same server, which is the default behaviour), you can add an ``authSource`` field to the index configuration object mapped to the name of the database the user used for authentication resides on (this is usefull when working with mlab-hosted MongoDB databases).

An example entry, including an extra keyword argument sent to the client's constructor:

.. code-block:: json

    ...
    "index": {
        "type": "MongoDB",
        "hosts": ["ds839662.mlab.com:25100"],
        "username": "dingle_idx_writer",
        "password": "$up3r5ecur3PA$$word",
        "db_name": "datascience_infra",
        "collection_name": "dinglebop_index",
        "authSource": "datascience_infra"
    },
    ...


Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.


Target future features
----------------------

* S3 store.
* Some SQL-based index. PostgreSQL?
* Redis-based cache.
* Consolidated dingles - Dingles based on the index and store served from the same server. Requires adding an abstraction to capture this architecture.
* S3-based consolidated dingle.


Installing for development
----------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:shaypal5/dinglebop.git


Install in development mode:

.. code-block:: bash

  cd dinglebop
  pip install -e .


Running the tests
-----------------

To run the tests use:

.. code-block:: bash

  pip install pytest pytest-cov coverage
  cd dinglebop
  pytest


Adding documentation
--------------------

The project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings. When documenting code you add to this project, follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Credits
=======

Created by Shay Palachy (shay.palachy@gmail.com).


.. |PyPI-Status| image:: https://img.shields.io/pypi/v/dinglebop.svg
  :target: https://pypi.python.org/pypi/dinglebop

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/dinglebop.svg
   :target: https://pypi.python.org/pypi/dinglebop

.. |Build-Status| image:: https://travis-ci.org/shaypal5/dinglebop.svg?branch=master
  :target: https://travis-ci.org/shaypal5/dinglebop

.. |LICENCE| image:: https://img.shields.io/pypi/l/dinglebop.svg
  :target: https://pypi.python.org/pypi/dinglebop

.. |Codecov| image:: https://codecov.io/github/shaypal5/dinglebop/coverage.svg?branch=master
   :target: https://codecov.io/github/shaypal5/dinglebop?branch=master
