from __future__ import annotations

import re
from decimal import Decimal
from pathlib import Path

import pymupdf


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving the full content."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_label(text: str, label: str, next_labels: list[str]) -> str:
    """
    Extract text after a label until the next known label or line break.
    """
    escaped_label = re.escape(label)
    following = "|".join(re.escape(item) for item in next_labels)

    pattern = rf"{escaped_label}\s*(.*?)(?=\s*(?:{following})|\n|$)"
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)

    if not match:
        raise ValueError(f"Could not find field: {label}")

    return match.group(1).strip()


def extract_pdf_text(pdf_path: str | Path) -> str:
    with pymupdf.open(pdf_path) as document:
        pages = [page.get_text("text", sort=True) for page in document]

    text = "\n".join(pages)

    if not text.strip():
        raise ValueError("No selectable text found. The PDF may require OCR.")

    return normalize_text(text)


def extract_trade(pdf_path: str | Path) -> dict:
    text = extract_pdf_text(pdf_path)

    result = {
        "type": extract_label(
            text,
            "Type",
            ["Execution", "Trading venue"],
        ),
        "execution": extract_label(
            text,
            "Execution",
            ["Trading venue"],
        ),
        "trading_venue": extract_label(
            text,
            "Trading venue",
            ["Securities account"],
        ),
        "securities_account": extract_label(
            text,
            "Securities account",
            ["Order ID"],
        ),
        "order_id": extract_label(
            text,
            "Order ID",
            ["Exchange ID"],
        ),
        "exchange_id": extract_label(
            text,
            "Exchange ID",
            ["Country of custody"],
        ),
        "country_of_custody": extract_label(
            text,
            "Country of custody",
            ["Kind of custody"],
        ),
        "kind_of_custody": extract_label(
            text,
            "Kind of custody",
            ["Type Security Quantity Price Amount"],
        ),
    }

    transaction_pattern = re.compile(
        r"""
        (?P<side>Buy|Sell)\s+
        (?P<security>.+?)\s+
        (?P<isin>[A-Z]{2}[A-Z0-9]{10})
        (?P<quantity>\d+(?:[.,]\d+))
        \s*pc\.?\s+
        (?P<price>\d+(?:[.,]\d{2}))
        \s+(?P<price_currency>[A-Z]{3})\s+
        (?P<amount>\d+(?:[.,]\d{2}))
        \s+(?P<amount_currency>[A-Z]{3})
        """,
        re.IGNORECASE | re.DOTALL | re.VERBOSE,
    )

    match = transaction_pattern.search(text)

    if not match:
        raise ValueError("Could not find the transaction row")

    transaction = match.groupdict()

    result.update(
        {
            "side": transaction["side"].capitalize(),
            "security": re.sub(r"\s+", " ", transaction["security"]).strip(),
            "isin": transaction["isin"].upper(),
            "quantity": Decimal(transaction["quantity"].replace(",", ".")),
            "price": Decimal(transaction["price"].replace(",", ".")),
            "price_currency": transaction["price_currency"].upper(),
            "amount": Decimal(transaction["amount"].replace(",", ".")),
            "amount_currency": transaction["amount_currency"].upper(),
        }
    )

    validate_trade(result)
    return result


def validate_trade(trade: dict) -> None:
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{10}", trade["isin"]):
        raise ValueError(f"Invalid ISIN: {trade['isin']}")

    if trade["quantity"] <= 0:
        raise ValueError("Quantity must be positive")

    if trade["price"] < 0 or trade["amount"] < 0:
        raise ValueError("Price and amount cannot be negative")

    if trade["price_currency"] != trade["amount_currency"]:
        raise ValueError("Price and amount currencies differ")


trade = extract_trade("I:\\Test\\rj4mEmh6t7PQCLqQ5vveKi.pdf")

for key, value in trade.items():
    print(f"{key}: {value}")
