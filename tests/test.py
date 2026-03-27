from src.easy_api_builder import ApiBuilder, easy_request

class TestApiBuilder():
    def setup_method(self):
        self.builder = ApiBuilder()

    def HostGetAPI(self):
        self.builder.get("/home", {"version": 1})

    def HostSecretAPI(self):
        self.builder.get("/secret", {"data": "top secret"}, auth_keys=["abc123"])

    def RunServer(self):
        self.builder.run()

t = TestApiBuilder()
t.setup_method()
t.HostGetAPI()
t.HostSecretAPI()
t.RunServer()





