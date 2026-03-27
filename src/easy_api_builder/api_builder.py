"""
A clean, efficient Flask-based API builder with authentication, routing, and error handling.
"""

from __future__ import annotations

import json
import logging
import threading
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import requests
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

__all__ = ("ApiBuilder", "easy_request")

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _json_error_handler(e: HTTPException):
    """Return all HTTP errors as JSON."""
    response = e.get_response()
    response.data = json.dumps(
        {"code": e.code, "name": e.name, "description": e.description}
    )
    response.content_type = "application/json"
    return response


def _require_api_key(valid_keys: List[str]) -> Callable:
    """Decorator that validates ?key= query param against *valid_keys*."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = request.args.get("key", "")
            if not key:
                return jsonify({"error": "API key required."}), 401
            if key not in valid_keys:
                return jsonify({"error": "Invalid API key."}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class ApiBuilder:
    """
    Fluent builder for simple Flask-based JSON APIs.

    Usage example::

        api = ApiBuilder()
        api.get("/hello", {"message": "Hello, world!"})
        api.get("/secret", {"data": "top secret"}, auth_keys=["abc123"])
        api.post("/submit", handler=my_handler)
        api.run()
    """

    def __init__(
        self,
        name: str = __name__,
        template_folder: str = "templates",
        debug: bool = False,
    ) -> None:
        self.app = Flask(name, template_folder=template_folder)
        self.debug = debug
        self._register_global_error_handlers()
        self._thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------
    # Route registration
    # ------------------------------------------------------------------

    def get(
        self,
        path: str = "/",
        payload: Any = None,
        *,
        auth_keys: Optional[List[str]] = None,
        handler: Optional[Callable] = None,
    ) -> "ApiBuilder":
        """
        Register a GET endpoint.

        :param path:      URL path (e.g. "/users").
        :param payload:   Static JSON-serialisable payload to return.
        :param auth_keys: Optional list of accepted API keys (?key=…).
        :param handler:   Optional callable ``() -> response`` that overrides *payload*.
        :returns: self  (fluent interface)
        """
        self._add_route(path, ["GET"], payload, auth_keys, handler)
        return self

    def post(
        self,
        path: str = "/",
        payload: Any = None,
        *,
        auth_keys: Optional[List[str]] = None,
        handler: Optional[Callable] = None,
    ) -> "ApiBuilder":
        """Register a POST endpoint (same signature as :meth:`get`)."""
        self._add_route(path, ["POST"], payload, auth_keys, handler)
        return self

    def route(
        self,
        path: str,
        methods: List[str],
        payload: Any = None,
        *,
        auth_keys: Optional[List[str]] = None,
        handler: Optional[Callable] = None,
    ) -> "ApiBuilder":
        """Register an endpoint for *any* HTTP methods."""
        self._add_route(path, [m.upper() for m in methods], payload, auth_keys, handler)
        return self

    # ------------------------------------------------------------------
    # Server lifecycle
    # ------------------------------------------------------------------

    def run(
        self,
        host: str = "0.0.0.0",
        port: int = 5000,
        threaded: bool = True,
    ) -> None:
        """Start the Flask development server (blocking)."""
        logger.info("Starting ApiBuilder server on %s:%s", host, port)
        self.app.run(host=host, port=port, debug=self.debug, threaded=threaded)

    def run_async(
        self,
        host: str = "0.0.0.0",
        port: int = 5000,
    ) -> threading.Thread:
        """
        Start the server in a *daemon* background thread.

        :returns: The :class:`threading.Thread` so callers can join/monitor it.
        """
        self._thread = threading.Thread(
            target=self.run,
            kwargs={"host": host, "port": port, "threaded": True},
            daemon=True,
            name="ApiBuilder-server",
        )
        self._thread.start()
        logger.info("ApiBuilder server thread started (port %s).", port)
        return self._thread

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _add_route(
        self,
        path: str,
        methods: List[str],
        payload: Any,
        auth_keys: Optional[List[str]],
        handler: Optional[Callable],
    ) -> None:
        """Core route-registration logic shared by all public helpers."""

        # Build a unique endpoint name to avoid Flask conflicts.
        endpoint = f"{'_'.join(methods).lower()}_{path.strip('/').replace('/', '_') or 'root'}"

        def view_func():
            if handler is not None:
                return handler()
            return jsonify(payload)

        # Wrap with auth decorator when keys are supplied.
        if auth_keys:
            view_func = _require_api_key(auth_keys)(view_func)

        # Give Flask a unique function name.
        view_func.__name__ = endpoint

        self.app.add_url_rule(path, endpoint=endpoint, view_func=view_func, methods=methods)

    def _register_global_error_handlers(self) -> None:
        """Attach JSON error handlers and a 404 HTML page."""

        self.app.register_error_handler(HTTPException, _json_error_handler)

        @self.app.errorhandler(404)
        def page_not_found(e):
            # Falls back to JSON when no template exists.
            try:
                return render_template("404.html"), 404
            except Exception:
                return jsonify({"code": 404, "name": "Not Found", "description": str(e)}), 404

        @self.app.errorhandler(400)
        def bad_request(e):
            return jsonify({"code": 400, "name": "Bad Request", "description": str(e)}), 400


# ---------------------------------------------------------------------------
# Standalone HTTP helper
# ---------------------------------------------------------------------------

def easy_request(
    url: str,
    method: str = "GET",
    *,
    params: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Thin wrapper around :mod:`requests` with sensible defaults.

    :param url:       Target URL.
    :param method:    HTTP verb (GET, POST, PUT, DELETE, …).
    :param params:    URL query parameters.
    :param json_body: Request body serialised as JSON.
    :param headers:   Extra request headers.
    :param timeout:   Socket timeout in seconds (default 10).
    :param api_key:   Appended as ``?key=<api_key>`` when provided.
    :returns:         Parsed JSON dict, or ``{"error": …}`` on failure.
    """
    method = method.upper()
    params = dict(params or {})
    if api_key:
        params["key"] = api_key

    try:
        response = requests.request(
            method,
            url,
            params=params or None,
            json=json_body,
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("easy_request timed out: %s", url)
        return {"error": "Request timed out.", "url": url}
    except requests.exceptions.HTTPError as exc:
        logger.error("HTTP error %s for %s", exc.response.status_code, url)
        return {"error": str(exc), "status_code": exc.response.status_code}
    except requests.exceptions.RequestException as exc:
        logger.error("Request failed: %s", exc)
        return {"error": str(exc)}
    except ValueError:
        # Response body is not JSON.
        return {"error": "Non-JSON response.", "body": response.text}
        