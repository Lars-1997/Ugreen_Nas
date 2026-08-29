import pymupdf
import pandas as pd


def extract_trade_data(pdf_path: str) -> pd.DataFrame:
    """Extract trade data from a PDF file."""
    doc = pymupdf.open(pdf_path)

    for page_idx, page in enumerate(doc):
        # Detect column boundaries from the header underline segments (or pass explicit x coordinates)
        header_rects = [
            d["rect"] for d in page.get_drawings() if 420 < d["rect"].y0 < 450
        ]
        v_lines = (
            sorted([r.x0 for r in header_rects] + [max(r.x1 for r in header_rects)])
            if header_rects
            else None
        )

        tabs = page.find_tables(vertical_lines=v_lines)

        # Extract text for key-value pairs
        text = page.get_text()
        lines = [line.strip() for line in text.split("\n")]

        extracted_data = {}
        key_mapping = {
            "Type": "ExecutionType",
            "Execution": "ExecutionDatetime",
            "Trading venue": "Trading Venue",
            "Order ID": "Order ID",
            "Exchange ID": "Exchange ID",
            "Country of custody": "Country of Custody",
        }

        found_keys = set()
        for i, line in enumerate(lines):
            if line in key_mapping and line not in found_keys:
                extracted_data[key_mapping[line]] = (
                    lines[i + 1] if i + 1 < len(lines) else None
                )
                found_keys.add(line)

        for table_idx, table in enumerate(tabs.tables):
            # print(f"--- Page {page_idx + 1} | Table {table_idx + 1} ---")
            # Extract directly to a pandas DataFrame
            df: pd.DataFrame = table.to_pandas()

            # Clean up empty rows
            df = df.replace("", None).dropna(how="all").reset_index(drop=True)

            # Split the security String into ISIN and Asset Name
            df[["AssetName", "ISIN"]] = df["Security"].str.split(
                "\\n",
                n=1,
                expand=True,
            )

            df = df.drop(columns=["Security"], errors="ignore")

            # Add extracted key-value pairs as new columns
            for col_name, value in extracted_data.items():
                df[col_name] = value

    # Rename columns to match the desired output format
    df = df.rename(
        columns={
            "Trading Venue": "TradingVenue",
            "Order ID": "OrderID",
            "Exchange ID": "ExchangeID",
            "Country of Custody": "CountryOfCustody",
            "ExecutionType": "OrderType",
            "Price": "CurrentMarketPrice",
            "Amount": "TotalValueInEUR",
        }
    )

    # Convert data types
    df["ExecutionDatetime"] = pd.to_datetime(
        df["ExecutionDatetime"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    # Convert numeric columns
    df["Quantity"] = df["Quantity"].str.removesuffix("pc.")
    df["Quantity"] = df["Quantity"].str.replace(r"[^0-9.,]+", "", regex=True)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["CurrentMarketPrice"] = df["CurrentMarketPrice"].str.replace(
        r"[^0-9.,]+", "", regex=True
    )
    df["CurrentMarketPrice"] = pd.to_numeric(df["CurrentMarketPrice"], errors="coerce")
    df["TotalValueInEUR"] = df["TotalValueInEUR"].str.replace(
        r"[^0-9.,]+", "", regex=True
    )
    df["TotalValueInEUR"] = pd.to_numeric(df["TotalValueInEUR"], errors="coerce")

    columns_order = [
        "OrderType",
        "Type",
        "ExecutionDatetime",
        "ISIN",
        "AssetName",
        "Quantity",
        "CurrentMarketPrice",
        "TotalValueInEUR",
        "TradingVenue",
        "ExchangeID",
        "OrderID",
        "CountryOfCustody",
    ]
    df = df[columns_order]
    return df
