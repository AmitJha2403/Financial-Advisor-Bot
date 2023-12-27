import os
import requests
import streamlit as st
import json
import logging
import subprocess

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

# Function to run a Python script and capture its output
def run_script(script_name):
    try:
        completed_process = subprocess.run(['python', script_name], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        st.write(f"{script_name} output:\n{completed_process.stdout}")
    except subprocess.CalledProcessError as e:
        st.error(f"Error running {script_name}: {e.stderr}")

# Initialize a session state variable for tracking the progress
if 'step' not in st.session_state:
    st.session_state['step'] = 0

# Streamlit app starts here
st.title('Stock Data Analysis Workflow')

# Predefined list of symbols for the dropdown
symbol_options = ['AAPL', 'IBM', 'GOOGL', 'MSFT', 'AMZN', 'BAC']
selected_symbol = st.selectbox('Select a symbol:', symbol_options)

# Fetch data step
if st.session_state['step'] == 0:
    if st.button('Fetch Data'):
        fetch_and_save_data(selected_symbol)
        st.session_state['step'] = 1

# Preprocess data step
if st.session_state['step'] == 1:
    if st.button('Run Preprocess'):
        run_script('preprocess.py')
        st.session_state['step'] = 2

# Merge data step
if st.session_state['step'] == 2:
    if st.button('Run Merge'):
        run_script('merge.py')
        st.session_state['step'] = 3

# Create models step
if st.session_state['step'] == 3:
    if st.button('Create Models'):
        run_script('models.py')
        st.session_state['step'] = 4

# Final prediction step
if st.session_state['step'] == 4:
    if st.button('Run Final Prediction'):
        run_script('final_prediction.py')
        st.session_state['step'] = 5

# Display current step to the user
st.write(f"Current Step: {st.session_state['step']}")