import os
from extract_trade_info import extract_trade_data
import pandas as pd

file_path = r"/app/skripts/pdf_files"
archive_path = rf"{file_path}/Archive"
os.makedirs(archive_path, exist_ok=True)
error_path = rf"{file_path}/Error"
os.makedirs(error_path, exist_ok=True)
destination_path = rf"{file_path}/Data"
os.makedirs(destination_path, exist_ok=True)
csv_file = destination_path + "/" + "trade_output.csv"

# Define primary keys for duplicate check
pk_columns = ["OrderType", "Type", "ExecutionDatetime", "ISIN"]

# Pre-load existing primary keys into a set for fast O(1) lookups
# This avoids reading the entire CSV repeatedly for every PDF
existing_keys = set()
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    try:
        # Load only the required columns to save memory
        existing_df = pd.read_csv(csv_file, usecols=lambda c: c in pk_columns)
        if "ExecutionDatetime" in existing_df.columns:
            existing_df["ExecutionDatetime"] = pd.to_datetime(
                existing_df["ExecutionDatetime"], errors="coerce"
            )

        available_pks = [col for col in pk_columns if col in existing_df.columns]
        if available_pks:
            existing_keys = set(
                existing_df[available_pks].itertuples(index=False, name=None)
            )
    except Exception as e:
        print(f"Warning: Could not read existing CSV for keys: {e}")


def transform_pdf_to_csv(file_path: str, csv_file: str) -> None:

    df = extract_trade_data(file_path)
    if df is None or df.empty:
        return

    # Ensure datetime formats align for accurate matching
    if "ExecutionDatetime" in df.columns:
        df["ExecutionDatetime"] = pd.to_datetime(
            df["ExecutionDatetime"], errors="coerce"
        )

    available_pks = [col for col in pk_columns if col in df.columns]

    if available_pks:
        is_new = []
        for row in df[available_pks].itertuples(index=False, name=None):
            if row in existing_keys:
                is_new.append(False)
            else:
                is_new.append(True)
                existing_keys.add(
                    row
                )  # Add new keys so they aren't duplicated in the same run

        df_new = df[is_new]
    else:
        df_new = df

    if not df_new.empty:
        write_header = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
        df_new.to_csv(csv_file, mode="a", header=write_header, index=False)
        print(f"Appended {len(df_new)} new transaction(s) to CSV.")
    else:
        print("Transaction already exists in CSV. Skipping.")


print(f"Starting script. Looking for PDFs in: {file_path}")
if not os.path.exists(file_path):
    print(f"Warning: Directory {file_path} does not exist!")
else:
    files = os.listdir(file_path)
    print(f"Found {len(files)} total files/directories in {file_path}")

for filename in os.listdir(file_path) if os.path.exists(file_path) else []:
    if filename.lower().endswith(".pdf"):
        print(f"Processing file: {filename}")
        try:
            pdf_file_path = os.path.join(file_path, filename)
            transform_pdf_to_csv(pdf_file_path, csv_file)
            os.replace(pdf_file_path, os.path.join(archive_path, filename))
            print(f"Successfully processed and archived: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            os.replace(pdf_file_path, os.path.join(error_path, filename))
