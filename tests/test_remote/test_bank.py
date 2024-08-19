import logging
from pprint import pprint

import pytest
from dynaconf import settings

from src.playground.bank.bank import Bank
from src.playground.bank import RestApiBank
from src.playground.items import Item
from src.rest_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)


@pytest.fixture
def bank() -> Bank:
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    maps: RestApiBank = RestApiBank(client=client)
    return maps


def test_items(bank: Bank):
    print(bank.get_bank_items())


def test_gold(bank: Bank):
    print(bank.get_bank_gold())


def test_item(bank: Bank):
    print(bank.get_bank_item(Item("copper_ore")))

def test_no_item(bank: Bank):
    print(bank.get_bank_item(Item("aboba")))
