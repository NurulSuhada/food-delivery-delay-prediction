import pandas as pd

def test_dataset_has_rows():
    df = pd.read_csv("order_history_kaggle_data.csv")
    assert len(df) > 0, "Dataset should not be empty"

def test_no_duplicate_records():
    df = pd.read_csv("order_history_kaggle_data.csv")
    assert df.duplicated().sum() == 0, "Dataset should not contain duplicate records"

def test_required_columns_exist():
    df = pd.read_csv("order_history_kaggle_data.csv")
    required_columns = [
        "Restaurant name",
        "City",
        "Order Status",
        "KPT duration (minutes)",
        "Rider wait time (minutes)"
    ]
    for col in required_columns:
        assert col in df.columns, f"Missing required column: {col}"
