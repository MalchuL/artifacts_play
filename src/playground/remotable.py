import requests
from requests.compat import urljoin


class Remotable:
    def __init__(self, api_host, api_token):
        self.api_host = api_host
        self.api_token = api_token
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    def request(
        self, host=None, endpoint="", method="GET", json=None, headers=None, params=None
    ) -> requests.Response:
        method = method.upper().strip()
        assert method in ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PUT", "PATCH"]
        if host is None:
            host = self.api_host
        if headers is None:
            headers = self.headers
        return requests.request(
            method=method, url=urljoin(host, endpoint), json=json, headers=headers, params=params
        )
