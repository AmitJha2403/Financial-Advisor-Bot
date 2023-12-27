# Financial-Advisor-Bot

This repository contains a series of Python scripts that form a workflow for stock data analysis. The workflow includes data fetching, preprocessing, merging, model creation, and making final predictions.

## Scripts Description

- `main.py`: The main Streamlit app script. It provides a user interface for the entire workflow, including data fetching, running preprocessing, merging, model creation, and final predictions.
- `getdata.py`: Responsible for fetching stock data using API requests and saving the data to files.
- `preprocess.py`: Handles preprocessing of the fetched stock data. It includes operations like filtering data based on date and cleaning.
- `merge.py`: Merges financial data with stock data and prepares it for model training.
- `models.py`: Creates machine learning models based on the preprocessed and merged data.
- `final_prediction.py`: Uses the created models to make final predictions and decision making.

## Workflow Steps

1. **Data Fetching**: Run `main.py` and use the Streamlit interface to fetch data for a selected stock symbol.
2. **Preprocessing**: After fetching the data, proceed to data preprocessing using `preprocess.py`.
3. **Merging Data**: Following preprocessing, merge the data with `merge.py`.
4. **Model Creation**: Create predictive models using `models.py`.
5. **Final Predictions**: Finally, run `final_prediction.py` to make predictions using the trained models.

## How to Run

1. Clone the repository.
2. Ensure all dependencies are installed: `requests`, `pandas`, `streamlit`, `sklearn`, `json`, `logging`.
3. Run the `main.py` script: `streamlit run main.py`.
4. Follow the Streamlit app interface to proceed through each step of the workflow.

## Dependencies

- Python 3
- Pandas
- Streamlit
- Scikit-learn
- Requests
- JSON
- Logging
