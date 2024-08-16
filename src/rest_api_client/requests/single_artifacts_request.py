import copy
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, List, Union, Optional

import httpx

from .artifacts_request import ArtifactsRequest
from .request import DataSchema, ResponseSchema
from ..client import Client, AuthenticatedClient
from ..errors import ArtifactsHTTPStatusError

IN = TypeVar('IN', bound=Optional[DataSchema])
OUT = TypeVar('OUT', bound=ResponseSchema)


class SingleArtifactsRequest(ArtifactsRequest, Generic[IN, OUT]):
    def __init__(self, client: Union[Client, AuthenticatedClient], **endpoint_kwargs):
        super().__init__(client=client)
        self.endpoint_kwargs = copy.deepcopy(endpoint_kwargs)

    @property
    @abstractmethod
    def method_name(self) -> str:
        pass

    @property
    @abstractmethod
    def response_schema(self) -> ResponseSchema.__class__:
        """
        :return: Returns pydantic Base
        """
        pass

    @property
    @abstractmethod
    def error_responses(self) -> Dict[int, str]:
        """
        :return: Mapping error_code: description
        """
        pass

    @property
    def success_responses(self) -> List[int]:
        """
        :return: Successful responses
        """
        return [200]

    def _endpoint_format_params(self):
        params = super()._endpoint_format_params()
        params.update(**self.endpoint_kwargs)
        return params

    def _make_request(self, method: str, data: IN = None) -> OUT:
        if method != self.method_name:
            raise ValueError(
                f"method {method} is not allowed for {self.__class__} class. Use {self.method_name} only")
        return super()._make_request(method, data)

    def _process_response(self, method: str, response: httpx.Response) -> ResponseSchema:
        data = self.response_schema.model_validate(response.json())
        return data

    def __call__(self, data: IN) -> OUT:
        assert isinstance(data, DataSchema) or data is None, f"In data is not {DataSchema} subclass, got {data}"
        return self._make_request(self.method_name, data)

    def _parse_error(self, response: httpx.Response):
        if response.status_code in self.error_responses:
            raise ArtifactsHTTPStatusError(
                response.status_code,
                content=str.encode(self.error_responses[response.status_code]),
                json=response.json())
        elif response.status_code not in self.success_responses:
            raise ArtifactsHTTPStatusError(
                response.status_code,
                content=str.encode(f"Unsupported error code:  {response.status_code} ") + response.content,
                json=response.json())
