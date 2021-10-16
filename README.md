Easy\_API\_Builder =========

An Python Package for easily create APIs in Python.

`pip install easy-api-builder`

Requiremnets: \<= python 3.6

Required modules --\> Flask, requests

Documentation
=============

Make an API with easy\_api\_builder:

```py
from easy_api_builder.builder import apiBuilder
json_response = \
{
    "easy_api_builder.Version": 0.1,
    "downloads": "200+"
}

builder = apiBuilder()
builder.create_get_api(json=json_response, url="/")
builder.start(port=80)
```

Make a Documentation Page for your API:

```py
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
builder.create_get_api(json=json_response, path="/")

# Create a Documentation Page for the API
builder.create_docs(sitename="Cocumentation", sitedescription="Official Documentation for easy_api API", path="/docs", docs="How to use our API? etc...")

# Start the API on defualt Port 80
builder.start(port=80)
```

Note: You can create only a Documentation Page too:

```py
# Import the Required Packages
from easy_api_builder.builder import apiBuilder
# Define the apiBuilder

builder = apiBuilder()

# Create a Documentation Page
builder.create_docs(sitename="Cocumentation", sitedescription="Official Documentation for easy_api API", path="/docs", docs="How to use our API? etc...")

# Start the API on defualt Port 80
builder.start(port=80)
```

You can change the path. For example "/api/v3"

**How to customize the Documentation- and Error Page?**

To customize the Documentation- and error page, go in the package folder
and edit the index.html and the 404.html
