import os
import PyPDF2
from extract_trade import extract_trade_data
import pandas as pd

file_path = r"C:\Users\larst\Downloads\dhLtKjojDL22dFvAeHzbse.pdf"
destination_path = r"I:\Test"
csv_file = destination_path + "\\" + "trade_output.csv"

with open(file_path, "rb") as file:
    pdf_reader = PyPDF2.PdfReader(file)
    page = pdf_reader.pages[0]
    text = page.extract_text()

data = extract_trade_data(text)
df = pd.DataFrame([data])
df = df.rename(
    columns={
        "Execution": "ExecutionDate",
        "Trading Venue": "TradingVenue",
        "Securities Account": "SecuritiesAccount",
        "Order ID": "OrderID",
        "Exchange ID": "ExchangeID",
        "Country of Custody": "CountryOfCustody",
        "Type": "OrderType",
        "Asset Name": "AssetObjectName",
        "ISIN": "ISIN",
        "Value After ISIN": "Quantity",
        "Value After pc": "CurrentMarketPrice",
        "Value After First EUR": "TotalValueInEUR",
    }
)

df["ExecutionDate"] = pd.to_datetime(
    df["ExecutionDate"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["CurrentMarketPrice"] = pd.to_numeric(df["CurrentMarketPrice"], errors="coerce")
df["TotalValueInEUR"] = pd.to_numeric(df["TotalValueInEUR"], errors="coerce")

columns_order = [
    "OrderType",
    "ExecutionDate",
    "TradingVenue",
    "ISIN",
    "AssetObjectName",
    "CurrentMarketPrice",
    "Quantity",
    "TotalValueInEUR",
    "SecuritiesAccount",
    "OrderID",
    "ExchangeID",
    "CountryOfCustody",
]
df = df[columns_order]

# Check if file exists and filter out already existing transactions based on primary keys
file_exists = os.path.exists(csv_file)
if file_exists:
    existing_df = pd.read_csv(csv_file)
    # Convert ExecutionDate back to datetime for accurate comparison
    if "ExecutionDate" in existing_df.columns:
        existing_df["ExecutionDate"] = pd.to_datetime(
            existing_df["ExecutionDate"], errors="coerce"
        )

    # Define primary keys for duplicate check
    pk_columns = ["OrderType", "ExecutionDate", "AssetObjectName"]

    # Merge or check if combination already exists
    merged = pd.concat([existing_df, df]).drop_duplicates(
        subset=pk_columns, keep="first"
    )

    # If the length is greater than existing_df, new rows were added
    if len(merged) > len(existing_df):
        # Get only the new rows by filtering out rows present in existing_df
        # Using merge with indicator=True to find rows unique to df
        df_new = pd.concat([existing_df, df]).drop_duplicates(
            subset=pk_columns, keep=False
        )
        # Actually, drop_duplicates(keep=False) drops both if duplicate. Better approach:
        df_new = df[
            ~df.set_index(pk_columns).index.isin(
                existing_df.set_index(pk_columns).index
            )
        ]

        if not df_new.empty:
            df_new.to_csv(csv_file, mode="a", header=False, index=False)
            print("New transaction appended to CSV.")
        else:
            print("Transaction already exists in CSV. Skipping.")
    else:
        print("Transaction already exists in CSV. Skipping.")
else:
    df.to_csv(csv_file, mode="w", header=True, index=False)
    print("CSV created and transaction appended.")
