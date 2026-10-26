from os import getenv
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()


def get_base_url(endpoint: str, withExchange: bool) -> str:
    return (
        f"https://api.databursatil.com/v2/{endpoint}?token={getenv('BMV_API_TOKEN')}"
        + ("&bolsa=bmv,biva" if withExchange else "")
    )


def request_prices(symbols: List[str]):
    response = requests.get(
        get_base_url("cotizaciones", withExchange=True)
        + "&concepto=u,p,a,x,n,c,m,v,o,i"
        + "&emisora_serie="
        + ",".join(symbols)
    )
    return response.json()


def request_currencies():
    response = requests.get(get_base_url("divisas", withExchange=False))
    return response.json()
