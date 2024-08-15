from dynaconf import settings
from requests.compat import urljoin

from src.playground.remotable import Remotable

END_POINT = "/my/characters"

def test_concat():
    assert urljoin(settings.API_HOST, "") == settings.API_HOST
    assert urljoin(settings.API_HOST, "my") == f"{settings.API_HOST}/my"
    assert urljoin(settings.API_HOST, "/my") == f"{settings.API_HOST}/my"


def test_remotable():
    remotable = Remotable(settings.API_HOST, settings.API_TOKEN)
    result = remotable.request(remotable.api_host, END_POINT)
    assert result.status_code == 200, result.json()
