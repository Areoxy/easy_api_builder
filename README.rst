Easy_API_Builder
================

A python package to easily create simple rest-apis in python.

``pip install easy-api-builder``

Requiremnets: <= python 3.6

Required modules –> Flask, requests

Documentation
=============

Build an API with easy_api_builder:

.. code:: py

   from easy_api_builder.builder import apiBuilder
   json_response = \
   {
       "easy_api_builder.Version": 0.1,
       "downloads": "200+"
   }

   builder = apiBuilder()
   builder.create_get_api(json_response, "/")
   builder.start(port=80)

Build an api with authorization by an api key

.. code:: py

   from easy_api_builder.builder import apiBuilder
   json_response = \
   {
       "easy_api_builder.Version": 0.1,
       "downloads": "200+"
   }

   builder = apiBuilder()
   builder.build_auth_api(json_response, ["key1", "key2], "/api/")
   builder.start(port=80)

To get a response from the api you must make a requests to this url:
http://yourdomain.com/api?key=key1/

Build a Documentation Page for your API:

.. code:: py

   # Import the required Packages
   from easy_api_builder.builder import apiBuilder

   json_response = \
   {
       "easy_api_builder.Version": 0.1,
       "downloads": "200+"
   }

   # Define the apiBuilder

   builder = apiBuilder()

   # Create a GET API
   builder.build_get_api(json=json_response, path="/")

   # Create a Documentation Page for the API
   builder.create_docs(sitename="Cocumentation", sitedescription="Official Documentation for easy_api API", path="/docs", docs="How to use our API? etc...")

   # Start the API on defualt Port 80
   builder.start(port=80)

Build a custom docs page

.. code:: {.py

   ...
   # Define the apiBuilder}
   builder = apiBuilder()

   builder.create_custom_docs("/docs/v3", "customfile.html")

   builder.start()

Note: You can create only a Documentation Page too:

.. code:: py

   # Import the Required Packages
   from easy_api_builder.builder import apiBuilder
   # Define the apiBuilder

   builder = apiBuilder()

   # Create a Documentation Page
   builder.create_docs(sitename="Cocumentation", sitedescription="Official Documentation for easy_api API", path="/docs", docs="How to use our API? etc...")

   # Start the API on defualt Port 80
   builder.start(port=80)

You can change the path. For example “/api/v3”

**How to customize the Documentation- and Error Page?**

To customize the Documentation- and error page, go in the package folder
and edit the index.html and the 404.html
