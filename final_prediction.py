import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from joblib import load

def prepare_data(new_data, include_financial_ratios=False):
    # Fill missing values in numeric columns with mean
    numeric_cols = new_data.select_dtypes(include=['float64', 'int64']).columns
    new_data[numeric_cols] = new_data[numeric_cols].fillna(new_data[numeric_cols].mean())

    # For non-numeric columns, fill with mode or a placeholder like 'Unknown'
    non_numeric_cols = new_data.select_dtypes(exclude=['float64', 'int64']).columns
    for col in non_numeric_cols:
        new_data[col] = new_data[col].fillna(new_data[col].mode()[0])

    # Calculate Financial Ratios if required
    if include_financial_ratios:
        new_data['current_ratio'] = new_data['totalCurrentAssets'] / new_data['totalCurrentLiabilities']
        new_data['debt_to_equity'] = new_data['totalLiabilities'] / new_data['totalShareholderEquity']

    # Calculate Technical Indicators
    new_data['moving_average_10'] = new_data['close'].rolling(window=10).mean()
    new_data['moving_average_50'] = new_data['close'].rolling(window=50).mean()

    # Feature Selection
    features = ['open', 'high', 'low', 'volume', 'moving_average_10', 'moving_average_50']
    if include_financial_ratios:
        features.extend(['current_ratio', 'debt_to_equity'])
    final_new_data = new_data[features]

    return final_new_data

def scale_and_impute(data):
    scaler = StandardScaler()
    imputer = SimpleImputer(strategy='mean')
    return scaler.fit_transform(imputer.fit_transform(data))

def make_predictions(model, data):
    return model.predict(data)

# Load models
models = {
    'BalanceSheetModel': load('BalanceSheetModel.joblib'),
    'CashFlowModel': load('CashFlowModel.joblib'),
    'EarningsModel': load('EarningsModel.joblib'),
    'IncomeModel': load('IncomeModel.joblib')
}

# Load and process data, then make predictions
predictions = {}
for model_name, model in models.items():
    file_path = f"merged_data_{model_name.split('Model')[0]}_StockData.csv"
    data = pd.read_csv(file_path)
    prepared_data = prepare_data(data, include_financial_ratios='BalanceSheet' in model_name)
    scaled_imputed_data = scale_and_impute(prepared_data)
    predictions[model_name] = make_predictions(model, scaled_imputed_data)

# Combine predictions
final_prediction = sum(predictions.values()) / len(predictions)

# Trading decisions
buy_threshold = 0.4
sell_threshold = -0.4
decisions = ["Buy" if prediction > buy_threshold else "Sell" if prediction < sell_threshold else "Hold" for prediction in final_prediction]

print(decisions[:10])
