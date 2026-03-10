# Step-by-Step Project Creation

## 1. Create project folder

Create a new folder for the assignment (e.g. `AdNabu-Assignment-Testing`).

## 2. Set up Python environment

Ensure Python 3 is installed. From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows: `.venv\Scripts\activate`

## 3. Add dependencies

Create `requirements.txt` with:

```
selenium>=4.15.0
webdriver-manager>=4.0.0
```

Install:

```bash
pip install -r requirements.txt
```

Chrome must be installed on the machine (webdriver-manager downloads the matching ChromeDriver).

## 4. Create manual test cases

Create `test_cases.txt`. Document:

- Store context (password-protected store, home page, sold-out behavior).
- **Product Search:** one positive (e.g. search using an in-stock product from home), one negative (invalid search), one edge (empty search). Each with steps and expected results.
- **Add to Cart:** one positive (add in-stock product), one negative (sold-out product), one edge (same product, multiple quantity). Each with steps and expected results.

Keep each case concise with bullet-point expected results.

## 5. Create automation script

Create `search_and_add_to_cart.py`.

**Config at top:** Store URL, store password, search fallback term, wait timeout, view delays.

**Driver:** Use `webdriver.Chrome` with `ChromeDriverManager().install()` and options (e.g. start-maximized). No headless.

**Flow as separate functions:**

1. **enter_store_password** – Wait for password input, send keys, click submit.
2. **wait_for_store_loaded** – Wait for any of: search input, main, header (multiple selectors in a loop).
3. **get_in_stock_product_search_term** – Find all `a[href*='/products/']` on the page. For each link, get a product card container (ancestor with class card/product/item). Skip if container text or a child contains "sold out", or has a sold-out class. Return the first in-stock product’s handle (from URL) as the search term (e.g. `product-name` → `product name`).
4. **search_product** – Optionally open search UI (e.g. click search icon). Find search input; if not found or not interactable, navigate to `STORE_URL/search?q=<query>`. Otherwise set value via JavaScript, submit form or send RETURN.
5. **wait_for_search_results** – Wait for product links or main/content.
6. **open_first_product** – Find `a[href*='/products/']`, skip collection links, click first visible (e.g. via JS click).
7. **wait_for_product_page** – Wait for Add to cart button (e.g. `button[name='add']` or similar).
8. **add_to_cart** – Find Add to cart button (multiple selectors), scroll into view, click (e.g. via JS). Fallback: XPath for button text containing "add to cart".
9. **wait_for_cart_updated** – Wait for any of: cart drawer, cart count element.
10. **run_scenario** – Call the above in order; after cart update, `time.sleep(VIEW_DELAY_SECONDS)`; in `finally`, `driver.quit()`.

Use only `WebDriverWait` and `expected_conditions` for waits; no `time.sleep` except for the optional view delay at the end (and any deliberate pause after search results).

## 6. Create run script

Create `run_automation.sh` (executable: `chmod +x run_automation.sh`):

- Change to script directory.
- If `.venv` does not exist, run `python3 -m venv .venv`.
- Activate venv, run `pip install -q -r requirements.txt`, then `python search_and_add_to_cart.py`.

## 7. Add .gitignore

Create `.gitignore` with:

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.webdriver-manager/
```

## 8. Add README

Create `README.md` with:

- Project title.
- Manual test cases: file name (`test_cases.txt`) and short description.
- Automation: script name (`search_and_add_to_cart.py`), what it does, how to run (`./run_automation.sh` or venv + pip commands), and that dependencies are in `requirements.txt` with Chrome required.

## 9. Run and verify

From the project folder:

```bash
./run_automation.sh
```

Or activate `.venv`, then `python search_and_add_to_cart.py`. Chrome should open, complete the flow (login → home → in-stock product search → open product → add to cart), then close after the view delay.

## 10. Version control (optional)

```bash
git init
git remote add origin <repo-url>
git add .gitignore README.md requirements.txt run_automation.sh search_and_add_to_cart.py test_cases.txt
git commit -m "Successfully done"
git push -u origin main
```

Do not add `.venv` or other ignored paths.
