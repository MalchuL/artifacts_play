from pydantic_core import to_json, from_json

from src.playground.utilites.build_resources_roadmap import NodeInfo


def test_pd_dataclass():
    info = NodeInfo()
    print(info.dict())
    print(from_json(to_json(info)))