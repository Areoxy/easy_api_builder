import flask 
import threading
import requests
from threading import *
from flask import *
import time
import werkzeug
from werkzeug import *
from werkzeug.exceptions import *
from werkzeug.exceptions import HTTPException
from typing import List


__all__ = ("apiBuilder", "easyRequest")

class apiBuilder():
    def __init__(self):
        """
        Represents a builder to create APIs
        """
        # Define Flask app

        __slots__ = ()

        self.app = Flask(__name__, template_folder='templates')

    def build_get_api(self, json, path="/"):
        """
        This function builds a "get" API on a custom url path

        :param json: The json response for the API
        :type: JSON
        :param path: The url path for the API
        :type: string
        """
        # App routes

        @self.app.route(f"{path}", methods=['GET'])
        def returnAPI():
            return jsonify(json)


        # Error Handling

        @self.app.errorhandler(werkzeug.exceptions.HTTPException)
        def handle_exception(e):
            # start with the correct headers and status code from the error
            response = e.get_response()
            # replace the body with JSON
            response.data = json.dumps({
                "code": e.code,
                "name": e.name,
                "description": e.description,
            })
            response.content_type = "application/json"
            return response

        # 404 error page
        
        @self.app.errorhandler(404)
        def page_not_found(e):
            # note that we set the 404 status explicitly
            return render_template('404.html'), 404

        
        # 400 Bad Request
        
        @self.app.errorhandler(werkzeug.exceptions.BadRequest)
        def handle_bad_request(e):
            return 'bad request!'
    
    def build_auth_api(self, json, keys: List, path="/"):
        """
        This function builds a "get" API by authorizing api key 

        :param json: The json response for the API
        :type: JSON
        :param path: The url path for the API
        :type: string
        :param keys: The List of keys wich will accepted 
        :type: List
        """
        # App routes

        @self.app.route(f"{path}", methods=['GET'])
        def returnAPI():
            key = request.args.get('key')
            if key in keys:
                return jsonify(json)
            else:
                return "Authorization by api key failed."


        # Error Handling

        @self.app.errorhandler(werkzeug.exceptions.HTTPException)
        def handle_exception(e):
            # start with the correct headers and status code from the error
            response = e.get_response()
            # replace the body with JSON
            response.data = json.dumps({
                "code": e.code,
                "name": e.name,
                "description": e.description,
            })
            response.content_type = "application/json"
            return response

        # 404 error page
        
        @self.app.errorhandler(404)
        def page_not_found(e):
            # note that we set the 404 status explicitly
            return render_template('404.html'), 404

        
        # 400 Bad Request
        
        @self.app.errorhandler(werkzeug.exceptions.BadRequest)
        def handle_bad_request(e):
            return 'bad request!'


    
    def create_docs(self, sitename: str, sitedescription: str, path: str, docs: str):
        """
        This function creates a documentation page for your API on a custom url path

        :param sitename: The sitename for the docs
        :param sitedescription: The site description
        :param path: The url path for example /docs/ (http://localhost/docs/)
        :param docs: The docs
        :type: string
        """

        @self.app.route(path)
        def documentation():
            return render_template("index.html", sitename=sitename, siteDescription=sitedescription, text=docs)
    
    def create_custom_docs(self, path: str, file: str):
        """
        This function creates a documentation page for your API with a custom html/css file as page.

        :param path: The url path for the documentation page
        :param file: The path to the custom html file as documentation page
        :type: string
        """

        @self.app.route(path)
        def documentation():
            return render_template(file)
    

    def start(self, port=80):
        """
        This function starts the api defaultly on port 80 (changeable)

        :param port: Sets the port on wich the api will run
        :type: integer
        """
        # Run App

        self.app.run(port=port, debug=True)
    
    def stop_api(self):
        """
        This function stops/deletes the api
        """
        # Delete/Stop API

        self.app.delete()


class easyRequest:
    def __init__(self):
        """
        Represents a builder for web requests
        """
        __slots__ = ()

    def get_request(self, url: str):
        """
        This function makes a get web requests 

        :param url: The url for the web requests
        :type: string
        """
        re = requests.get(url=url)
        json_response = re.json()
        return json_response

        