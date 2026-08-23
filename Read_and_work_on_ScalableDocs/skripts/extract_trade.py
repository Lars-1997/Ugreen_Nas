import re


def extract_trade_data(text):
    # Regex patterns or parsing logic based on the requested fields:
    # - Trading Venue
    # - Securities Account
    # - Order ID
    # - Exchange ID
    # - Country of Custody
    # - Type (e.g., LIMIT or Buy/Sell)
    # - Execution
    # - Value after Buy (Asset Name)
    # - ISIN
    # - Value after ISIN (Quantity / Amount right after ISIN before pc.)
    # - Value after pc. (Quantity / Price components or specifically quantity / price)
    # - Value after the first EUR (Price or Amount)

    data = {}

    # Execution
    exec_match = re.search(
        r"Execution\s+(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text
    )
    data["Execution"] = exec_match.group(1) if exec_match else None

    # Trading venue
    venue_match = re.search(r"Trading venue\s+([A-Z0-9]+)", text)
    data["Trading Venue"] = venue_match.group(1) if venue_match else None

    # Securities account & Order ID
    # Note: "Securities account 5164436117Order ID SCALC1aqmomzuQR"
    account_match = re.search(r"Securities account\s+(\d+)(?:Order ID\s+(\w+))?", text)
    if account_match:
        data["Securities Account"] = account_match.group(1)
        data["Order ID"] = account_match.group(2)
    else:
        data["Securities Account"] = None
        data["Order ID"] = None

    # Exchange ID
    exchange_match = re.search(r"Exchange ID\s+(\w+)", text)
    data["Exchange ID"] = exchange_match.group(1) if exchange_match else None

    # Country of Custody
    country_match = re.search(
        r"Country of custody\s+([A-Za-z\s]+?)(?:Kind of custody|$)", text
    )
    data["Country of Custody"] = (
        country_match.group(1).strip() if country_match else None
    )

    # Type (e.g. LIMIT or Buy)
    type_match = re.search(r"^Type\s+(\w+)", text, re.MULTILINE)
    data["Type"] = type_match.group(1) if type_match else None

    # Value after Buy (Asset name)
    buy_match = re.search(r"Buy\s+(.+?)(?=\s+LU\d)", text)
    data["Asset Name"] = buy_match.group(1).strip() if buy_match else None

    # ISIN
    isin_match = re.search(r"(LU\d{10})", text)
    data["ISIN"] = isin_match.group(1) if isin_match else None

    # Value after ISIN (Quantity / Amount right after ISIN before pc.)
    after_isin_match = re.search(r"LU\d{10}([0-9\.]+)\s+pc\.", text)
    data["Value After ISIN"] = after_isin_match.group(1) if after_isin_match else None

    # Value after pc.
    pc_match = re.search(r"pc\.\s+([0-9\.]+)\s+EUR", text)
    data["Value After pc"] = pc_match.group(1) if pc_match else None

    # Value after the first EUR
    eur_matches = re.findall(r"([0-9\.]+)\s+EUR", text)
    data["Value After First EUR"] = (
        eur_matches[1]
        if len(eur_matches) > 1
        else (eur_matches[0] if eur_matches else None)
    )

    return data
