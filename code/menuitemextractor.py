if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


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



if __name__=='__main__':
    test_items = [
        '''
NEW!

Tully Tots

$11.79

Made from scratch with shredded potatoes, cheddar-jack cheese and Romano cheese all rolled up and deep-fried. Served with a spicy cheese sauce.
        ''',

        '''Super Nachos

$15.49
GS

Tortilla chips topped with a mix of spicy beef and refried beans, nacho cheese sauce, olives, pico de gallo, jalapeños, scallions and shredded lettuce. Sour cream and salsa on the side. Add guacamole $2.39

        ''',
        '''Veggie Quesadilla

$11.99
V

A flour tortilla packed with cheese, tomatoes, jalapeños, black olives and scallions. Served with sour cream and pico de gallo.
Add chicken $2.99 | Add guacamole $2.39
''',
'''Kid's Burger & Fries

$6.99
'''

    ]
    title = "TEST"
    for scraped_text in test_items:
        item = extract_menu_item(title, scraped_text)
        print(item)