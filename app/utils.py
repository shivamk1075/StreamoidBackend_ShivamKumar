import csv
from io import StringIO

REQUIRED_FIELDS = ["sku", "name", "brand", "mrp", "price"]


def parse_csv(file_stream):
    text = file_stream.read().decode("utf-8")
    reader = csv.DictReader(StringIO(text))
    rows = list(reader)
    return rows


def validate_row(row):
    errors = []
    # required
    for f in REQUIRED_FIELDS:
        if not row.get(f):
            errors.append(f"missing_{f}")

    try:
        mrp = float(str(row.get("mrp", "0")).strip())
    except Exception:
        errors.append("invalid_mrp")
        mrp = None
    try:
        price = float(str(row.get("price", "0")).strip())
    except Exception:
        errors.append("invalid_price")
        price = None
    try:
        quantity = int(str(row.get("quantity", "0")).strip()) if row.get("quantity") not in (None, "") else 0
    except Exception:
        errors.append("invalid_quantity")
        quantity = None

    if mrp is not None and price is not None:
        if price > mrp:
            errors.append("price_gt_mrp")

    if quantity is not None:
        if quantity < 0:
            errors.append("quantity_negative")

    return len(errors) == 0, errors, {
        "mrp": mrp,
        "price": price,
        "quantity": quantity,
    }
