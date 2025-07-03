import logging
from abc import abstractmethod
from typing import Union

from attr import evolve

from src.rest_api_client.client import Client, AuthenticatedClient
from src.rest_api_client.errors import ArtifactsHTTPStatusError
from .request import HTTPRequest, DataSchema, ResponseSchema
import httpx


logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 3

class ArtifactsRequest(HTTPRequest):
    default_headers = {"Content-Type": "application/json",
                       "Accept": "application/json"}

    def __init__(self, client: Union[Client, AuthenticatedClient], retries=3):
        self._client = client
        self._retries = retries

    def get(self) -> ResponseSchema:
        return self._make_request("get")

    def post(self, schema: DataSchema) -> ResponseSchema:
        return self._make_request("post", data=schema)

    def update(self, schema: DataSchema) -> ResponseSchema:
        return self._make_request("update", data=schema)

    def delete(self, schema: DataSchema) -> ResponseSchema:
        return self._make_request("delete", data=schema)

    def _make_request(self, method: str, data: DataSchema = None):
        method = method.lower()
        assert method in ["get", "post", "delete", "update"]
        if method == "get" or data is None:
            assert data is None
            json_data = None
        else:
            json_data = data.model_dump()
        for i in range(self._retries):
            try:
                with evolve(self._client) as client:
                    url = self.get_endpoint()
                    response = client.get_httpx_client().request(method=method, url=url,
                                                                 headers=self.get_headers(),
                                                                 timeout=DEFAULT_TIMEOUT,
                                                                 json=json_data)
                    break
            except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                logger.error(
                    f"Error in sending request {dict(method=method, url=url, headers=self.get_headers(), json=json_data)}, {e}")
                logger.error(f"Number of retries {i}/{self._retries}")
        self._parse_error(response)
        return self._process_response(method=method, response=response)

    @abstractmethod
    def _process_response(self, method: str, response: httpx.Response) -> ResponseSchema:
        """
        Creates from response from _make_request ResponseSchema. Should raise error on bad status
         code. Should process all methods if they defined, e.g "get" and "post"
        :param str method: method of sent request, [get, post, delete, update]
        :param httpx.Response response: HTTP Response
        :return: parsed by pydantic data from response
        """
        pass

    def _parse_error(self, response: httpx.Response):
        if response.status_code != 200:
            raise ArtifactsHTTPStatusError(response.status_code, content=response.content,
                                           json=response.json())
