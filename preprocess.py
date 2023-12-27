import pandas as pd
import json

def preprocess_csv(file_path, start_date, end_date):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    filtered_df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    filtered_df.to_csv(file_path, index=False)

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"No file found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return None

def save_json_file(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except IOError:
        print(f"Error writing JSON to {file_path}")

def preprocess_json(file_path, key_to_remove):
    data = read_json_file(file_path)
    if data and key_to_remove in data:
        del data[key_to_remove]
        save_json_file(data, file_path)

# Preprocess Time Series Dataset
preprocess_csv('TIME_SERIES.csv', '2018-09-28', '2023-09-29')

# Preprocess JSON datasets
datasets = {
    'BALANCE_SHEET.json': 'annualReports',
    'CASH_FLOW.json': 'annualReports',
    'EARNINGS.json': 'annualEarnings',
    'INCOME_STATEMENT.json': 'annualReports'
}

for file_path, key in datasets.items():
    preprocess_json(file_path, key)
