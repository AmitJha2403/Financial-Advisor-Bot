import pandas as pd
import json

def merge_financial_data_with_stock(json_file_path, stock_file_path, json_data_key, output_file_name):
    # Load and prepare financial data
    with open(json_file_path, 'r') as file:
        financial_data = json.load(file)
    financial_df = pd.DataFrame(financial_data[json_data_key])
    financial_df['fiscalDateEnding'] = pd.to_datetime(financial_df['fiscalDateEnding'])
    
    # Load and prepare stock data
    stock_data = pd.read_csv(stock_file_path)
    stock_data['timestamp'] = pd.to_datetime(stock_data['timestamp'])
    
    # Merging logic
    merged_data = []
    for index, stock_row in stock_data.iterrows():
        filtered_financial = financial_df[financial_df['fiscalDateEnding'] >= stock_row['timestamp']]
        if not filtered_financial.empty:
            latest_financial = filtered_financial.iloc[-1]
            merged_row = {**stock_row.to_dict(), **latest_financial.to_dict()}
            merged_data.append(merged_row)
    
    # Create a DataFrame from the merged data and save it
    merged_df = pd.DataFrame(merged_data)
    merged_df.to_csv(output_file_name, index=False)

# Define the file paths and keys for each dataset
datasets = [
    ('BALANCE_SHEET.json', 'TIME_SERIES.csv', "quarterlyReports", "merged_data_BalanceSheet_StockData.csv"),
    ('CASH_FLOW.json', 'TIME_SERIES.csv', "quarterlyReports", "merged_data_CashFlow_StockData.csv"),
    ('EARNINGS.json', 'TIME_SERIES.csv', "quarterlyEarnings", "merged_data_Earnings_StockData.csv"),
    ('INCOME_STATEMENT.json', 'TIME_SERIES.csv', "quarterlyReports", "merged_data_Income_StockData.csv")
]

# Process each dataset
for json_file, stock_file, data_key, output_file in datasets:
    merge_financial_data_with_stock(json_file, stock_file, data_key, output_file)
