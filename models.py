import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump

def process_and_train_model(file_path, model_name, include_financial_ratios=False):
    # Load data
    data = pd.read_csv(file_path)

    # Separate numeric and non-numeric columns
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    non_numeric_cols = data.select_dtypes(exclude=['float64', 'int64']).columns

    # Fill missing values
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
    for col in non_numeric_cols:
        data[col] = data[col].fillna(data[col].mode()[0])

    # Financial Ratios (Optional)
    if include_financial_ratios:
        data['current_ratio'] = data['totalCurrentAssets'] / data['totalCurrentLiabilities']
        data['debt_to_equity'] = data['totalLiabilities'] / data['totalShareholderEquity']

    # Technical Indicators
    data['moving_average_10'] = data['close'].rolling(window=10).mean()
    data['moving_average_50'] = data['close'].rolling(window=50).mean()

    # Selecting features
    features = ['open', 'high', 'low', 'close', 'volume', 'moving_average_10', 'moving_average_50']
    if include_financial_ratios:
        features += ['current_ratio', 'debt_to_equity']

    final_data = data[features]

    # Scale data
    scaler = StandardScaler()
    final_data_scaled = scaler.fit_transform(final_data)

    # Prepare data for model
    close_column_index = final_data.columns.get_loc("close")
    X = np.delete(final_data_scaled, close_column_index, axis=1)  # Remove 'close' column
    y = final_data_scaled[:, close_column_index]                  # Set 'close' as the target variable
    nan_mask = ~np.isnan(y)
    X, y = X[nan_mask], y[nan_mask]

    # Impute missing values in features
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Model: {model_name} - MSE: {mse}, R2 Score: {r2}")

    # Save the model
    dump(model, f'{model_name}.joblib')

# Define the file paths and model names
datasets = [
    ('merged_data_BalanceSheet_StockData.csv', 'BalanceSheetModel', True),
    ('merged_data_CashFlow_StockData.csv', 'CashFlowModel', False),
    ('merged_data_Earnings_StockData.csv', 'EarningsModel', False),
    ('merged_data_Income_StockData.csv', 'IncomeModel', False)
]

# Process each dataset
for file_path, model_name, include_financial_ratios in datasets:
    process_and_train_model(file_path, model_name, include_financial_ratios)
