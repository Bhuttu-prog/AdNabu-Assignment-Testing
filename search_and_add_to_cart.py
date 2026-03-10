import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

STORE_URL = "https://adnabu-store-assignment1.myshopify.com"
STORE_PASSWORD = "AdNabuQA"
SEARCH_QUERY = "shirt"
WAIT_TIMEOUT = 15
VIEW_DELAY_SECONDS = 8
SEARCH_VIEW_DELAY_SECONDS = 5


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def enter_store_password(driver, wait):
    password_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'], input[name='password']"))
    )
    password_input.send_keys(STORE_PASSWORD)
    submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
    submit.click()


def wait_for_store_loaded(driver, wait):
    for sel in [
        "input[name='q']",
        "input[type='search']",
        ".search-input",
        "[role='search'] input",
        "form[action*='search'] input",
        "main",
        "#MainContent",
        "header",
    ]:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            return
        except Exception:
            continue


def get_in_stock_product_search_term(driver, wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/products/']")))
    product_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")
    for link in product_links:
        href = link.get_attribute("href") or ""
        if "collections" in href or "/products/" not in href:
            continue
        try:
            container = link
            try:
                container = link.find_element(By.XPATH, "(./ancestor::*[contains(@class, 'card') or contains(@class, 'product') or contains(@class, 'item')])[1]")
            except Exception:
                pass
            container_text = (container.get_attribute("innerText") or container.text or "").lower()
            if "sold out" in container_text:
                continue
            try:
                sold_out_el = container.find_element(By.XPATH, ".//*[contains(translate(text(), 'SOLD OUT', 'sold out'), 'sold out')]")
                if sold_out_el.is_displayed():
                    continue
            except Exception:
                pass
            try:
                container.find_element(By.CSS_SELECTOR, "[class*='sold-out'], .sold-out")
                continue
            except Exception:
                pass
            if link.is_displayed():
                handle = href.split("/products/")[-1].split("?")[0].strip("/")
                if handle:
                    return handle.replace("-", " ")
                link_text = (link.get_attribute("innerText") or link.text or "").strip()
                if link_text and len(link_text) < 100:
                    return link_text
                return href.split("/products/")[-1].split("?")[0].replace("-", " ")
        except Exception:
            continue
    if product_links:
        href = product_links[0].get_attribute("href") or ""
        return href.split("/products/")[-1].split("?")[0].replace("-", " ")
    return SEARCH_QUERY


def open_search_if_needed(driver, wait):
    for sel in [
        "a[href*='/search']",
        "button[aria-label*='earch']",
        ".header__search",
        "[data-search-open]",
        "summary[aria-controls*='search']",
        "details.modal__toggle",
        ".search-modal__button",
        "details-disclosure[data-search] summary",
    ]:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            if el.is_displayed():
                el.click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='q'], input[type='search']")))
                return
        except Exception:
            continue


def search_product(driver, wait, query):
    open_search_if_needed(driver, wait)
    search_selectors = [
        "input[name='q']",
        "input[type='search']",
        ".search-input",
        "[role='search'] input",
        "form[action*='search'] input",
    ]
    search_input = None
    for sel in search_selectors:
        try:
            search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            if search_input.is_displayed():
                break
        except Exception:
            continue
    if not search_input:
        driver.get(STORE_URL.rstrip("/") + "/search?q=" + query)
        return
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_input)
    try:
        search_input.click()
    except Exception:
        pass
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", search_input, query)
    try:
        form = search_input.find_element(By.XPATH, "./ancestor::form")
        form.submit()
    except Exception:
        search_input.send_keys(Keys.RETURN)


def wait_for_search_results(driver, wait):
    for sel in [
        "a[href*='/products/']",
        ".product-item",
        ".product-card",
        "[class*='product']",
        ".search-results",
        "main",
    ]:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            return
        except Exception:
            continue


def open_first_product(driver, wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/products/']")))
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")
    for link in links:
        href = link.get_attribute("href") or ""
        if "/products/" in href and "collections" not in href:
            try:
                if link.is_displayed():
                    driver.execute_script("arguments[0].click();", link)
                    return
            except Exception:
                continue
    if links:
        driver.execute_script("arguments[0].click();", links[0])
        return
    raise Exception("No product link found in search results")


def wait_for_product_page(driver, wait):
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[name='add'], input[name='add'], [name='add-to-cart'], .add-to-cart, [data-add-to-cart]"))
    )


def add_to_cart(driver, wait):
    add_selectors = [
        "button[name='add']",
        "input[name='add']",
        "[name='add-to-cart']",
        ".add-to-cart",
        "[data-add-to-cart]",
        "button[type='submit']",
        "form[action*='cart'] button",
        "form[action*='cart'] input[type='submit']",
    ]
    for sel in add_selectors:
        try:
            btns = driver.find_elements(By.CSS_SELECTOR, sel)
            for btn in btns:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", btn)
                    return
        except Exception:
            continue
    add_buttons = driver.find_elements(By.XPATH, "//button[contains(translate(., 'ADD TO CART', 'add to cart'), 'add to cart')]")
    if not add_buttons:
        add_buttons = driver.find_elements(By.XPATH, "//input[@type='submit' and contains(translate(@value, 'ADD TO CART', 'add to cart'), 'add to cart')]")
    for b in add_buttons:
        if b.is_displayed():
            driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", b)
            return
    raise Exception("Add to cart button not found or not clickable")


def wait_for_cart_updated(driver, wait):
    for selector in [
        ".drawer__header",
        ".cart-drawer",
        "[class*='cart-drawer']",
        ".cart-count",
        ".cart-item-count",
        "#cart-count",
    ]:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return
        except Exception:
            continue


def run_scenario():
    driver = create_driver()
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    try:
        driver.get(STORE_URL)
        enter_store_password(driver, wait)
        wait_for_store_loaded(driver, wait)
        search_term = get_in_stock_product_search_term(driver, wait)
        search_product(driver, wait, search_term)
        wait_for_search_results(driver, wait)
        time.sleep(SEARCH_VIEW_DELAY_SECONDS)
        open_first_product(driver, wait)
        wait_for_product_page(driver, wait)
        add_to_cart(driver, wait)
        wait_for_cart_updated(driver, wait)
        time.sleep(VIEW_DELAY_SECONDS)
        return True
    finally:
        driver.quit()


if __name__ == "__main__":
    success = run_scenario()
    exit(0 if success else 1)
