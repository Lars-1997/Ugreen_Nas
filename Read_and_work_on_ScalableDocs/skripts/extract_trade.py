# import re


# def extract_trade_data(text: str) -> dict:
#     # Regex patterns or parsing logic based on the requested fields:
#     # - Trading Venue
#     # - Securities Account
#     # - Order ID
#     # - Exchange ID
#     # - Country of Custody
#     # - Type (e.g., LIMIT or Buy/Sell)
#     # - Execution
#     # - Value after Buy (Asset Name)
#     # - ISIN
#     # - Value after ISIN (Quantity / Amount right after ISIN before pc.)
#     # - Value after pc. (Quantity / Price components or specifically quantity / price)
#     # - Value after the first EUR (Price or Amount)

#     data = {}

#     # Execution
#     exec_match = re.search(
#         r"Execution\s+(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text
#     )
#     data["Execution"] = exec_match.group(1) if exec_match else None

#     # Trading venue
#     venue_match = re.search(r"Trading venue\s+([A-Z0-9]+)", text)
#     data["Trading Venue"] = venue_match.group(1) if venue_match else None

#     # Securities account & Order ID
#     account_match = re.search(r"Securities account\s+(\d+)", text)
#     data["Securities Account"] = account_match.group(1) if account_match else None

#     order_match = re.search(r"Order ID\s+(.+?)(?=\s*Exchange ID|\n|$)", text)
#     data["Order ID"] = order_match.group(1).strip() if order_match else None

#     # Exchange ID
#     exchange_match = re.search(r"Exchange ID\s+(\w+)", text)
#     data["Exchange ID"] = exchange_match.group(1) if exchange_match else None

#     # Country of Custody
#     country_match = re.search(
#         r"Country of custody\s+([A-Za-z\s]+?)(?:Kind of custody|$)", text
#     )
#     data["Country of Custody"] = (
#         country_match.group(1).strip() if country_match else None
#     )

#     # Type (e.g. LIMIT or Buy)
#     type_match = re.search(r"^Type\s+(\w+)", text, re.MULTILINE)
#     data["Type"] = type_match.group(1) if type_match else None

#     # Value after Buy (Asset name)
#     buy_match = re.search(
#         r"Buy\s+(.+?)(?=\s+(?:IE|LU|DE|FR|US|GB|CH|NL)[A-Z0-9]{10})", text
#     )
#     data["Asset Name"] = buy_match.group(1).strip() if buy_match else None

#     # ISIN (ETFs commonly domiciled in IE, LU, DE, FR, US, GB, CH, NL, etc.)
#     isin_match = re.search(r"((?:IE|LU|DE|FR|US|GB|CH|NL)[A-Z0-9]{10})", text)
#     data["ISIN"] = isin_match.group(1) if isin_match else None

#     # Value after ISIN (Quantity / Amount right after ISIN before pc.)
#     after_isin_match = re.search(
#         r"(?:IE|LU|DE|FR|US|GB|CH|NL)[A-Z0-9]{10}([0-9\.]+)\s+pc\.", text
#     )
#     data["Value After ISIN"] = after_isin_match.group(1) if after_isin_match else None

#     # Value after pc.
#     pc_match = re.search(r"pc\.\s+([0-9\.]+)\s+EUR", text)
#     data["Value After pc"] = pc_match.group(1) if pc_match else None

#     # Value after the first EUR
#     eur_matches = re.findall(r"([0-9\.]+)\s+EUR", text)
#     data["Value After First EUR"] = (
#         eur_matches[1]
#         if len(eur_matches) > 1
#         else (eur_matches[0] if eur_matches else None)
#     )

#     return data
import re


def extract_trade_data(text: str) -> dict:
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
    account_match = re.search(r"Securities account\s+(\d+)", text)
    data["Securities Account"] = account_match.group(1) if account_match else None

    order_match = re.search(r"Order ID\s+(.+?)(?=\s*Exchange ID|\n|$)", text)
    data["Order ID"] = order_match.group(1).strip() if order_match else None

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

    # Asset Name (text right after Buy up until the next line or numbers/ISIN)
    buy_match = re.search(
        r"Buy\s+([^\n\r]+?)(?=\s*(?:[A-Z]{2}[A-Z0-9]{10}|\d+\.\d+\s*pc\.|\n|\r|$))",
        text,
    )
    data["Asset Name"] = buy_match.group(1).strip() if buy_match else None

    # ISIN (Exactly 2 letters followed by 10 alphanumeric characters)
    isin_match = re.search(r"([A-Z]{2}[A-Z0-9]{10})", text)
    data["ISIN"] = isin_match.group(1) if isin_match else None

    # Quantity / Value after ISIN (handles ISIN glued to quantity e.g. LU09085007530.154059 pc. or separate)
    qty_match = re.search(
        r"(?:[A-Z]{2}[A-Z0-9]{10}\s*|^|\s)(\d+(?:\.\d+)?)\s*pc\.", text, re.MULTILINE
    )
    data["Value After ISIN"] = qty_match.group(1) if qty_match else None

    # Price / Value after pc.
    pc_match = re.search(r"pc\.\s*([\d\.,]+)\s*EUR", text)
    data["Value After pc"] = pc_match.group(1) if pc_match else None

    # Amount / Value after First EUR (the second amount followed by EUR in the trade line)
    amount_match = re.search(r"pc\.\s*[\d\.,]+\s*EUR\s*([\d\.,]+)\s*EUR", text)
    data["Value After First EUR"] = amount_match.group(1) if amount_match else None

    return data
