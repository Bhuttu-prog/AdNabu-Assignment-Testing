# AdNabu QA Assignment

## Manual test cases

**File:** `test_cases.txt`

Contains 6 test cases for Product Search and Add to Cart (positive, negative, and edge). Includes expected results and steps for AdNabuTestStore (password: AdNabuQA).

---

## Automation

**Script:** `search_and_add_to_cart.py`

**What it does:** Logs into the store, finds an in-stock product on the home page, searches for it, opens the first result, and adds it to the cart. Uses Python and Selenium with explicit waits (no hardcoded sleeps).

**Run:**

```bash
./run_automation.sh
```

Or with a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python search_and_add_to_cart.py
```

**Dependencies:** Listed in `requirements.txt` (selenium, webdriver-manager). Chrome must be installed.

**Test reports:** Each run writes a report to `reports/automation_report_YYYY-MM-DD_HH-MM-SS.txt` with status (PASS/FAIL), duration, search term, steps, and error details if failed. The script prints the report path when it finishes.
