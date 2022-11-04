import pandas as pd
from prefect import flow, task
from prefect.blocks.system import Secret
import requests
import PyHyperScattering

@task
def get_stock_data():
    secret_block = Secret.load("alpha-vantage")

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    api_key = secret_block.get()
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    return data

@task
def transform_data(data):
    return data["Time Series (Daily)"]

@flow
def lab103():
    data = get_stock_data()
    ts_data = transform_data(data)


if __name__ == "__main__":
    lab103()