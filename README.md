# easy-api-builder

A lightweight Flask wrapper for building JSON APIs without boilerplate. Register endpoints, authentication, and error handling in a single fluent call, then consume any API with the built-in `easy_request` helper.

---

## Installation

```bash
pip install easy-api-builder
```
---

## Quick start

```python
from api_builder import ApiBuilder, easy_request

api = ApiBuilder()

api.get("/status", {"ok": True})
api.run()
```

Visit `http://localhost:5000/status` — done.

---

## ApiBuilder

### Constructor

```python
api = ApiBuilder(
    name=__name__,         # Flask app name
    template_folder="templates",  # folder for HTML error pages
    debug=False,           # enable Flask debug mode
)
```

### Registering endpoints

All registration methods return `self`, so calls can be chained.

#### `.get(path, payload, *, auth_keys, handler)`

```python
# Static payload
api.get("/hello", {"message": "Hello, world!"})

# Key-protected
api.get("/secret", {"data": 42}, auth_keys=["abc123", "xyz789"])

# Custom handler
def my_handler():
    from flask import jsonify, request
    return jsonify({"echo": request.args.get("q")})

api.get("/echo", handler=my_handler)
```

#### `.post(path, payload, *, auth_keys, handler)`

Same signature as `.get()`, registers a POST endpoint.

```python
from flask import jsonify, request

def handle_submit():
    body = request.get_json()
    return jsonify({"received": body})

api.post("/submit", handler=handle_submit)
```

#### `.route(path, methods, payload, *, auth_keys, handler)`

Register any HTTP verb or combination of verbs.

```python
api.route("/ping", ["GET", "POST"], {"pong": True})
```

### Starting the server

```python
# Blocking — use for production-style scripts
api.run(host="0.0.0.0", port=5000)

# Non-blocking daemon thread — use when running alongside other code
thread = api.run_async(port=5000)
```

---

## Authentication

Pass `auth_keys` to any registration method. Requests must include `?key=<value>` in the URL.

```python
api.get("/private", {"data": "secret"}, auth_keys=["abc123"])
```

| Scenario | Status | Response |
|---|---|---|
| No key supplied | `401` | `{"error": "API key required."}` |
| Wrong key | `403` | `{"error": "Invalid API key."}` |
| Valid key | `200` | Your payload |

---

## Error handling

All HTTP errors are returned as JSON automatically — no setup required.

```json
{
  "code": 404,
  "name": "Not Found",
  "description": "..."
}
```

If a `templates/404.html` file exists it will be rendered for 404s; otherwise the JSON fallback is used.

---

## easy_request

A thin wrapper around `requests` with built-in error handling.

```python
easy_request(
    url,               # target URL (required)
    method="GET",      # HTTP verb
    params=None,       # URL query parameters (dict)
    json_body=None,    # request body sent as JSON (dict)
    headers=None,      # extra headers (dict)
    timeout=10,        # socket timeout in seconds
    api_key=None,      # appended as ?key= automatically
)
```

Returns a parsed JSON dict on success, or a safe error dict on failure.

```python
# Simple GET
data = easy_request("https://api.example.com/users")

# Authenticated
data = easy_request("http://localhost:5000/secret", api_key="abc123")

# POST with body
data = easy_request(
    "http://localhost:5000/submit",
    method="POST",
    json_body={"name": "Alice"},
)
```

### Error responses

```python
{"error": "Request timed out.",  "url": "..."}          # timeout
{"error": "...",  "status_code": 403}                   # HTTP error
{"error": "Non-JSON response.",  "body": "..."}          # non-JSON body
```

---

## Full example

```python
from flask import jsonify, request
from api_builder import ApiBuilder, easy_request

api = ApiBuilder()

# Public status endpoint
api.get("/status", {"ok": True})

# Protected data endpoint
api.get("/data", {"value": 99}, auth_keys=["secret-key"])

# Dynamic POST handler
def echo():
    return jsonify(request.get_json())

api.post("/echo", handler=echo)

# Start in background thread
api.run_async(port=5000)

# Consume the protected endpoint
result = easy_request("http://localhost:5000/data", api_key="secret-key")
print(result)  # {"value": 99}
```

---

## License

MIT
