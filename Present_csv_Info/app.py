from flask import Flask, render_template, request, jsonify
import pandas as pd
from pathlib import Path

app = Flask(__name__)

CSV_PATH = Path("data/sample.csv")


def load_data():
    """Load CSV into DataFrame"""
    if not CSV_PATH.exists():
        return None
    return pd.read_csv(CSV_PATH)


@app.route("/")
def home():
    """Main page with table"""
    df = load_data()
    if df is None:
        return "CSV file not found", 404

    # Get unique values for dropdown filters
    unique_values = {}
    for col in df.columns:
        if df[col].nunique() < 10:  # Only for low-cardinality columns
            unique_values[col] = sorted(df[col].unique().astype(str).tolist())

    return render_template(
        "index.html",
        columns=df.columns.tolist(),
        row_count=len(df),
        unique_values=unique_values,
    )


@app.route("/api/data")
def api_data():
    """API endpoint for DataTables AJAX"""
    df = load_data()
    if df is None:
        return jsonify({"error": "No data"}), 404

    # DataTables parameters
    draw = int(request.args.get("draw", 1))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))
    search_value = request.args.get("search[value]", "")

    # Column search
    for i, col in enumerate(df.columns):
        col_search = request.args.get(f"columns[{i}][search][value]", "")
        if col_search:
            df = df[df[col].astype(str).str.contains(col_search, case=False, na=False)]

    # Global search
    if search_value:
        mask = pd.Series([False] * len(df))
        for col in df.columns:
            mask |= df[col].astype(str).str.contains(search_value, case=False, na=False)
        df = df[mask]

    # Sorting
    order_columns = []
    order_dirs = []
    for i in range(5):  # DataTables supports up to 5 sort columns
        order_col = request.args.get(f"order[{i}][column]")
        order_dir = request.args.get(f"order[{i}][dir]")
        if order_col is not None:
            order_columns.append(int(order_col))
            order_dirs.append(order_dir)

    if order_columns:
        sort_cols = [df.columns[i] for i in order_columns]
        ascending = [d == "asc" for d in order_dirs]
        df = df.sort_values(by=sort_cols, ascending=ascending)

    # Filtered count
    filtered_count = len(df)

    # Pagination
    df_page = df.iloc[start : start + length]

    # Convert to list of lists for DataTables
    data = df_page.values.tolist()

    return jsonify(
        {
            "draw": draw,
            "recordsTotal": len(load_data()),
            "recordsFiltered": filtered_count,
            "data": data,
        }
    )


@app.route("/api/columns")
def api_columns():
    """Return column definitions for DataTables"""
    df = load_data()
    if df is None:
        return jsonify([]), 404

    columns = []
    for col in df.columns:
        col_type = "text"
        if "date" in col.lower() or "at" in col.lower():
            col_type = "date"
        elif (
            "amount" in col.lower() or "price" in col.lower() or "value" in col.lower()
        ):
            col_type = "num"

        columns.append({"data": col, "title": col, "type": col_type})

    return jsonify(columns)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
