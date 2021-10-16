[![Downloads](https://static.pepy.tech/personalized-badge/easy-api-builder?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/easy-api-builder) [![Code Quality](https://www.code-inspector.com/project/29418/status/svg)

Easy-API-Builder
=========

An Python Package for easily create APIs in Python

`pip install easy-api-builder`

Requiremnets: \<= python 3.6

Required modules --> Flask 

Documentation
-------------

Make an API and Docs with easy_api_builder

```py

from easy_api_builder import EasyAPI

json = {
   "api_version": 0.1,
   "bot_version": 1.2.3
}

app = EasyAPI()
app.start(json, "<h1>Docs</h1>","Sitename", "siteDescription", "/")

```

The API runs on default localhost port 80 (localhost/)

You can replace the / with you path to the API Site.

The Docs can you find under localhost/docs

**How to customize?**

To customize the Documentation and error page, go in the package folder
and edit the index.html and the 404.html
