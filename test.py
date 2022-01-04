from easy_api_builder.builder import apiBuilder, easyRequest

json_response = \
{
    "easy_api_builder.Version": 0.1,
    "downloads": "200+"
}

builder = apiBuilder()
api = builder.build_auth_api(json_response, ["key", "key2"], "/")
builder.start(port=80)



