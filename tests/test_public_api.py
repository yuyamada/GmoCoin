#!python3
from pprint import pprint
from enum import Enum

from src.gmocoin.public.api import Client
from src.gmocoin.public.dto import Status, Symbol

def test_get_status(capfd):
    client = Client()
    res = client.get_status()

    assert type(res.status) is int
    assert type(res.responsetime) is str
    assert type(res.data.status) is Status

    print(res.status)
    print(res.responsetime)
    print(res.data.status)


def test_get_ticker(capfd):
    client = Client()
    res = client.get_ticker(Symbol.BTC_JPY)

    assert type(res.status) is int
    assert type(res.responsetime) is str
    for d in res.data:
        assert type(d.ask) is float
        assert type(d.bid) is float
        assert type(d.high) is float
        assert type(d.last) is float
        assert type(d.low) is float
        assert type(d.symbol) is Symbol
        assert type(d.timestamp) is str
        assert type(d.volume) is float
        
        print(d.ask)
        print(d.bid)
        print(d.high)
        print(d.last)
        print(d.low)
        print(d.symbol)
        print(d.timestamp)
        print(d.volume)

    res = client.get_ticker()

    symbol_list = [s for s in Symbol]
    assert len(res.data) == len(symbol_list)
    for d in res.data:
        assert d.symbol in symbol_list
