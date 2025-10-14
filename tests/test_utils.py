import io
from app.utils import parse_csv, validate_row


def test_parse_and_validate_good_row():
    csv_text = "sku,name,brand,color,size,mrp,price,quantity\nTSHIRT-RED-001,Classic Cotton T-Shirt,Stream Threads,Red,M,799,499,20\n"
    f = io.BytesIO(csv_text.encode("utf-8"))
    rows = parse_csv(f)
    assert len(rows) == 1
    ok, errors, parsed = validate_row(rows[0])
    assert ok
    assert errors == []
    assert parsed["mrp"] == 799.0
    assert parsed["price"] == 499.0
    assert parsed["quantity"] == 20


def test_validate_missing_required():
    row = {"sku": "", "name": "A", "brand": "B", "mrp": "100", "price": "90"}
    ok, errors, parsed = validate_row(row)
    assert not ok
    assert any(e.startswith("missing_") for e in errors)


def test_invalid_price_gt_mrp():
    row = {"sku": "1", "name": "A", "brand": "B", "mrp": "100", "price": "150", "quantity": "1"}
    ok, errors, parsed = validate_row(row)
    assert not ok
    assert "price_gt_mrp" in errors
