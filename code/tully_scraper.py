import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd
from dataclasses import dataclass, asdict

@dataclass
class MenuItem:
    # these are built-in properties
    category: str
    name: str
    price: float
    description: str

    # convert to a dictionary
    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return MenuItem(**data)
    
if __name__=='__main__':
    # example of howto use the dataclass

    # create a new MenuItem    
    mozz = MenuItem(name = "Mozzarella Sticks", 
                    price = 8.99, 
                    category="Apps", 
                    description="Fried cheese sticks served with marinara sauce.")

    # can assign a new category
    mozz.category = "Appetizers"
    print(mozz)
    # convert back to a dictionary
    print(mozz.to_dict())

    # create a new MenuItem from a dictionary
    burger = MenuItem.from_dict({"name": "Burger", 
                                 "price": 9.99, 
                                 "description": "A delicious burger.", 
                                 "category": "Entrees"})
    print(burger)

def clean_price(price:str) -> float:
    price = price.replace("$", "")
    price = price.replace(",", "")
    return float(price)

def clean_scraped_text(scraped_text: str) -> list[str]:
    items = scraped_text.split("\n")
    cleaned = []
    for item in items:
        if item in ['GS', "V", "S", "P"] or item.startswith("NEW") or len(item.strip()) == 0:
            continue
        if item.startswith("NEW"):
            continue 
        if len(item.strip()) == 0:
            continue 
        cleaned.append(item.strip())

    return cleaned

def extract_menu_item(title:str, scraped_text: str) -> MenuItem:
    cleaned_items = clean_scraped_text(scraped_text)
    item = MenuItem(category=title, name="", price=0.0, description="")
    item.name = cleaned_items[0]
    item.price = clean_price(cleaned_items[1])
    if len(cleaned_items) > 2:
        item.description = cleaned_items[2]
    else:
        item.description = "No description available."
    return item


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
