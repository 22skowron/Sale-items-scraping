from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint
import json
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

URL = "https://misbhv.com/pl/en/misbhv-seasonal-sale/men"

driver = webdriver.Chrome(chrome_options)
driver.get(url=URL)
driver.maximize_window()
time.sleep(1)



####################################################################################
def rename_duplicate(duplicate_name, items_in_total: int):
    for x in range(items_in_total):
        if f"[{x}]" in duplicate_name:
            new_name = duplicate_name.replace(f"[{x}]", f"[{x + 1}]")
            return new_name

    new_name = duplicate_name + " [2]"
    return new_name

#####################################################################################

    # Accept cookies
cookies_btn = driver.find_element(By.CSS_SELECTOR, ".amgdprcookie-button.-allow")
cookies_btn.click()
time.sleep(1)

    # Main mechanism
# item_divs = driver.find_elements(By.CSS_SELECTOR, ".product-item-details")
items_dict = {}
item_divs = []
last_height = driver.execute_script("return document.body.scrollHeight")
loop_count = 0
n = 0

while True:
    loop_count += 1
    print(f"Loop number: {loop_count}")

    # Scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    # Find strived-for inf.
    current_item_divs = driver.find_elements(By.CSS_SELECTOR, ".product-item-details")

    newly_added_count = 0
    for item in current_item_divs:

        if item not in item_divs:
            item_divs.append(item)
            newly_added_count += 1

            # Name:
            item_name = item.find_element(By.CSS_SELECTOR, ".product-item-name").text
            # Check if a product with a similar name is already in the dict, rename if present
            while items_dict.get(item_name):
                item_name = rename_duplicate(duplicate_name=item_name, items_in_total=len(items_dict))
            n += 1
            print(f"{n}. {item_name}")


            # Price:
            try:
                sold_out = item.find_element(By.CSS_SELECTOR, ".product-item-label-wrapper.comingsoon").text
                items_dict.update({
                    item_name: {
                        "Unfortunately": sold_out,
                    }
                })

            except NoSuchElementException:
                price_old = item.find_element(By.CSS_SELECTOR, ".old-price").text
                price_new = item.find_element(By.CSS_SELECTOR, ".normal-price").text
                items_dict.update({
                    item_name: {
                        "price_old": price_old,
                        "price_new": price_new
                    }
                })
    print(f"\nFound: {len(current_item_divs)}\n"
          f"Newly added: {newly_added_count},\n"
          f"Items in total: {len(items_dict)}\n")

    # End the process if no more data to load
    print(f"Current body scrollHeight: {last_height}")
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(f"New body scrollHeight: {new_height}\n")
    if new_height == last_height:
        break
    last_height = new_height


# Print results and save to json
items_count = {
    "Items found:": len(items_dict)
}

print(f"\n{items_count}")

with open("misbhv_items.json", "w") as file:
    json.dump([items_count, items_dict], file, indent=4)


time.sleep(2)
driver.quit()





