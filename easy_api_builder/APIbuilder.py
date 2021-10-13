import flask 
from flask import * 
import time
from werkzeug.exceptions import HTTPException




class EasyApi():
    def __init__(self):
        pass

    def  start(self, json, text: str, sitename: str, siteDescription, type="t", port=80, url="/"):
        # Define Flask app
        self.app = Flask(__name__, template_folder='templates')
        self.port = port

        # App routes

        @self.app.route(f"{url}", methods=['GET'])
        def returnAPI():
            return jsonify(json)
        

        # Check if docs are found
        
        if type == "t":
            @self.app.route("/docs", methods=['GET'])
            def docs():
                return render_template("index.html", sitename=sitename, siteDescription=siteDescription, text=text)
        else:
            print("No Documentation found.")

        # Error Handling

        @app.errorhandler(HTTPException)
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
        
        @app.errorhandler(404)
        def page_not_found(e):
            # note that we set the 404 status explicitly
            return render_template('404.html'), 404

        
        # Run App on default port 80

        if __name__ == '__main__':
            self.app.run(port=self.port, debug=True)
    
    def stop(self):
        self.app.delete()

        