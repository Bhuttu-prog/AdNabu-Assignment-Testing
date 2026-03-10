# Step-by-Step Project Creation from Scratch

## How to execute each step

| Step | Where | What to do |
|------|--------|------------|
| 1 | **Terminal** | Run the bash commands in a terminal. |
| 2 | **Editor** | Create and edit `test_cases.txt` in your editor (Cursor/VS Code, etc.). |
| 3 | **Editor** then **Terminal** | Create `requirements.txt` in editor; then in terminal run the venv and pip commands. |
| 4 | **Editor** | Create and edit `search_and_add_to_cart.py` in your editor. |
| 5 | **Editor** then **Terminal** | Create `run_automation.sh` in editor; then in terminal run `chmod +x run_automation.sh`. |
| 6 | **Editor** | Create and edit `README.md` in your editor. |
| 7 | **Terminal** | Run the git commands in a terminal (optional). |
| 8 | **Terminal** | Run `./run_automation.sh` or the Python command in a terminal. |

---

## 1. Create project directory

**Execute in: Terminal**

```bash
mkdir testFold
cd testFold
```

## 2. Define manual test cases

**Execute in: Editor** (create new file `test_cases.txt` and type or paste content)

Create `test_cases.txt` with the test scenarios:

- Document store URL, password, and behavior (password-protected store, home page products, search, add to cart).
- Add Product Search cases: positive (in-stock product search), negative (invalid search), edge (empty search).
- Add Add to Cart cases: positive (add in-stock product), negative (out-of-stock), edge (multiple quantity).
- For each case include: Steps, Expected results.

## 3. Set up Python environment

**Execute in: Editor** for `requirements.txt` (create file and add the two lines).  
**Then in Terminal:** run the three commands (venv, activate, pip install).  
**Chrome:** install from browser vendor if not already installed (no terminal command).

Create `requirements.txt` with dependencies:

```
selenium>=4.15.0
webdriver-manager>=4.0.0
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ensure Chrome is installed on the machine (webdriver-manager will use it).

## 4. Implement the automation script

**Execute in: Editor** (create new file `search_and_add_to_cart.py` and write the Python code)

Create `search_and_add_to_cart.py`.

**4.1 Imports and constants**

- Import: `time`, `selenium.webdriver`, `By`, `Keys`, `WebDriverWait`, `expected_conditions`, `Service`, `ChromeDriverManager`.
- Define: `STORE_URL`, `STORE_PASSWORD`, `SEARCH_QUERY` (fallback), `WAIT_TIMEOUT`, optional view delays.

**4.2 Driver setup**

- Implement `create_driver()`: use `ChromeOptions` (e.g. start-maximized, disable automation flags), `Service(ChromeDriverManager().install())`, return `webdriver.Chrome(service=..., options=...)`.

**4.3 Store login**

- Implement `enter_store_password(driver, wait)`: wait for password input (e.g. `input[type='password']` or `input[name='password']`), send password, find and click submit (e.g. `input[type='submit']` or `button[type='submit']`).

**4.4 Store loaded**

- Implement `wait_for_store_loaded(driver, wait)`: try a list of selectors (search input, main, header, etc.) with `wait.until(EC.presence_of_element_located(...))` until one succeeds.

**4.5 In-stock product from home**

- Implement `get_in_stock_product_search_term(driver, wait)`: wait for product links `a[href*='/products/']`, filter out collection links, skip cards that contain "sold out" (text or class), return product handle or name from first in-stock link; fallback to first product or `SEARCH_QUERY`.

**4.6 Search**

- Implement `open_search_if_needed(driver, wait)`: try selectors for search trigger (e.g. search link, search button, header search), click if visible, then wait for search input.
- Implement `search_product(driver, wait, query)`: call `open_search_if_needed`, find search input with a list of selectors, scroll into view, set value (e.g. via JS `value` + `input` event), submit form or send Enter; if no input found, navigate to `STORE_URL/search?q=<query>`.
- Implement `wait_for_search_results(driver, wait)`: wait for one of product links, product card, search results, or main content.

**4.7 Product page and add to cart**

- Implement `open_first_product(driver, wait)`: wait for product links, find first visible link with `/products/` and not `collections`, click via JS; fallback to first link.
- Implement `wait_for_product_page(driver, wait)`: wait for add-to-cart button (e.g. `button[name='add']`, `input[name='add']`, `.add-to-cart`, `[data-add-to-cart]`).
- Implement `add_to_cart(driver, wait)`: try add-button selectors, scroll into view and click first visible; then try XPath for "add to cart" text on buttons/inputs; raise if none found.
- Implement `wait_for_cart_updated(driver, wait)`: wait for one of cart drawer, cart count, or cart-related element.

**4.8 Main flow**

- Implement `run_scenario()`: create driver and `WebDriverWait(driver, WAIT_TIMEOUT)`; in try/finally (quit in finally): get store URL, enter password, wait for store, get search term from in-stock product, search, wait for results, optional sleep, open first product, wait for product page, add to cart, wait for cart update, optional sleep; return True.
- Under `if __name__ == "__main__"`: call `run_scenario()`, exit 0 on success else 1.

## 5. Add run script

**Part A — Editor:** Create a new file named `run_automation.sh` in the project folder. Put this exact content in the file (these are not commands you type in the terminal; they are the lines that will run when you execute the script later):

```bash
#!/usr/bin/env bash
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
. .venv/bin/activate
pip install -q -r requirements.txt
python search_and_add_to_cart.py
```

Save the file.

**Part B — Terminal (one time):** From the project folder, run this so the script is allowed to execute:

```bash
chmod +x run_automation.sh
```

**Part C — Terminal (whenever you want to run the automation):** From the project folder, run:

```bash
./run_automation.sh
```

That command runs the script: it ensures a virtual environment exists, activates it, installs dependencies, and runs the Python automation.

## 6. Add README

**Execute in: Editor** (create new file `README.md` and add the content)

Create `README.md` with:

- Project title and short description.
- Reference to manual test cases file and what it contains.
- Automation section: script name, what it does (login, find in-stock product, search, open first result, add to cart; Selenium, explicit waits).
- Run instructions: `./run_automation.sh` and alternate venv/pip/python commands.
- Dependencies (requirements.txt) and Chrome requirement.

## 7. Optional: version control

**Execute in: Terminal** (run each command in order)

```bash
git init
echo ".venv/" >> .gitignore
git add requirements.txt run_automation.sh search_and_add_to_cart.py test_cases.txt README.md PROJECT_CREATION_STEPS.md
git commit -m "Initial project"
```

## 8. Run and verify

**Execute in: Terminal**

- Run: `./run_automation.sh` (or activate venv and run `python search_and_add_to_cart.py`).
- Confirm browser opens, store loads, password is entered, an in-stock product is found, search runs, first result opens, add to cart works, and script exits with code 0.
