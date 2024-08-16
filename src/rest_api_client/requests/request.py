from abc import abstractmethod, ABC
from typing import Dict

from pydantic import BaseModel

DataSchema = BaseModel
ResponseSchema = BaseModel


class HTTPRequest(ABC):

    @property
    @abstractmethod
    def endpoint_pattern(self) -> str:  # e.g. "/my/{name}/action/move"
        pass

    @property
    @abstractmethod
    def default_headers(self) -> Dict[str, str]:
        pass

    def get_headers(self) -> Dict:
        headers = self.default_headers.copy()
        headers.update(self._additional_headers())
        return headers

    def _additional_headers(self) -> Dict:
        return {}

    def _endpoint_format_params(self):
        return {}

    def get_endpoint(self):
        return self.endpoint_pattern.format(**self._endpoint_format_params())

    def get(self) -> ResponseSchema:
        raise NotImplementedError(self.__error_message("get"))

    def post(self, schema: DataSchema) -> ResponseSchema:
        raise NotImplementedError(self.__error_message("post"))

    def update(self, schema: DataSchema) -> ResponseSchema:
        raise NotImplementedError(self.__error_message("update"))

    def delete(self, schema: DataSchema) -> ResponseSchema:
        raise NotImplementedError(self.__error_message("delete"))

    @classmethod
    def __error_message(cls, method_name):
        return f"{method_name} is not implemented for {cls.__name__} class"
