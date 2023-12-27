import os
import requests
import streamlit as st
import json
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Function to make API requests
def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
    return None

# Function to save data to a file
def save_data(file_name, data, is_json=False):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)

        with open(file_name, 'w', newline='') as file:
            if is_json:
                json.dump(data, file)
            else:
                file.write(data)
        st.write(f"Data for '{file_name}' saved successfully.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        st.write("Failed to save data.")

# Function to fetch and save data for a symbol
def fetch_and_save_data(symbol):
    api_key = 'LE13V7DH2CDOC269'
    tasks = {
        "TIME_SERIES": f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}&datatype=csv',
        "OVERVIEW": f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}',
        "INCOME_STATEMENT": f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}',
        "BALANCE_SHEET": f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}',
        "CASH_FLOW": f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}',
        "EARNINGS": f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}',
        "NEWS_SENTIMENT": f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={symbol}&time_from=20180928T0000&time_to=20230929T0000&limit=1000&apikey={api_key}'
    }

    for task_name, url in tasks.items():
        response = make_api_request(url)
        if response:
            file_extension = 'json' if 'json' in response.headers.get('Content-Type', '') else 'csv'
            file_name = f'{task_name}.{file_extension}'
            save_data(file_name, response.json() if file_extension == 'json' else response.text, is_json=(file_extension == 'json'))

# Streamlit app starts here
st.title('Fetch Stock Data')

# Predefined list of symbols for the dropdown
symbol_options = ['AAPL', 'IBM', 'GOOGL', 'MSFT', 'AMZN', 'BAC']

selected_symbol = st.selectbox('Select a symbol:', symbol_options)

if st.button('Fetch Data'):
    fetch_and_save_data(selected_symbol)
