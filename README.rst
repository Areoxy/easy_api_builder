Easy\_API\_Builder 
=================

An Python Package for easily create APIs in Python.

`pip install easy-api-builder`

Requiremnets: <= python 3.6

Required modules --> Flask, requests

.. code:: python
      from easy_api_builder.builder import apiBuilder, easyRequest

      json_response = \
      {
          "easy_api_builder.Version": 0.1,
          "downloads": "200+"
      }

      builder = apiBuilder()
      api = builder.create_get_api(json=json_response, url="/")
      builder.start(port=80)
