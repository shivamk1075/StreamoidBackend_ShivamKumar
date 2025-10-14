import traceback
import sys
from pathlib import Path

# ensure project root on path for imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.test_utils import (
    test_parse_and_validate_good_row,
    test_validate_missing_required,
    test_invalid_price_gt_mrp,
)


def run(fn):
    try:
        fn()
        print(f"PASS: {fn.__name__}")
    except AssertionError:
        print(f"FAIL: {fn.__name__}")
        traceback.print_exc()


if __name__ == "__main__":
    run(test_parse_and_validate_good_row)
    run(test_validate_missing_required)
    run(test_invalid_price_gt_mrp)
