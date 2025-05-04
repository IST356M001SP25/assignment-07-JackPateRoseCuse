import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")

    extracted_items = []
    for title in page.query_selector_all("h3.foodmenu__menu-section-title"):
        title_text = title.inner_text()
        print("MENU SECTION:", title_text) 
        row = title.query_selector("~ *").query_selector("~ *")
        for item in row.query_selector_all("div.foodmenu__menu-item"):
            item_text = item.inner_text()
            extracted_item = extract_menu_item(title_text, item_text)
            print(f"  MENU ITEM: {extracted_item.name}")
            extracted_items.append(extracted_item.to_dict())

    df = pd.DataFrame(extracted_items)
    df.to_csv("cache/tullys_menu.csv", index=False)

    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)
