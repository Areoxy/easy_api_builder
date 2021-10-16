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


class apiBuilder():
    def __init__(self):
        # Define Flask app

        self.app = Flask(__name__, template_folder='templates')

    def create_get_api(self, json, path="/"):
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

    
    def create_docs(self, sitename: str, sitedescription: str, path: str, docs: str):
        @self.app.route(path)
        def documentation():
            return render_template("index.html", sitename=sitename, siteDescription=sitedescription, text=docs)
    

    def start(self, port=80):
        # Run App

        self.app.run(port=port, debug=True)
    
    def stop_api(self):
        # Delete/Stop API

        self.app.delete()


class easyRequest:
    def __init__(self):
        pass

    def get_request(self, url: str):
        re = requests.get(url=url)
        json_response = re.json()
        return json_response

        