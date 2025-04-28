from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Path to your ChromeDriver
driver_path = "C:\\Users\\Acer\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"


# List of store names to search
stores = [
    "The Sleep Company Dwarka Sec-12",
    "The Sleep Company Kirti Nagar",
    "The Sleep Company Jail Road",
    "The Sleep Company Lajpat Nagar",
    "The Sleep Company Golf Course Road",
    "The Sleep Company Ghitorni",
    "The Sleep Company South Ex",
    "The Sleep Company Noida sec 17",
    "The Sleep Company Pebble Downtown Mall Faridabad",
    "The Sleep Company Rohini",
    "The Sleep Company Model Town",
    "The Sleep Company Preet Vihar",
    "The Sleep Company Indirapuram",
    "The Sleep Company Airia Mall Sec 68 Gurugram",
    "The Sleep Company Gaur City",
    "The Sleep Company Ghaziabad Sec 15",
    "The Sleep Company Andheri West",
    "The Sleep Company Ghatkopar West",
    "The Sleep Company Bandra Linking Road",
    "The Sleep Company Borivali West"
]

# Start the browser
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Create list for data
all_reviews = []

for store in stores:
    print(f"Searching for {store}...")
    driver.get("https://www.google.com/maps")
    time.sleep(3)

    # Search for the store
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()
    search_box.send_keys(store)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    try:
        # Click on the reviews button
        reviews_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, ' reviews')]")
        reviews_button.click()
        time.sleep(5)

        # Scroll to load reviews
        review_section = driver.find_element(By.CLASS_NAME, "m6QErb")
        for _ in range(3):  # Scroll a few times to load latest
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', review_section)
            time.sleep(2)

        # Get reviews
        reviews = driver.find_elements(By.CLASS_NAME, "jftiEf")[:5]  # Take latest 5

        for r in reviews:
            try:
                reviewer = r.find_element(By.CLASS_NAME, "d4r55").text
                review_text = r.find_element(By.CLASS_NAME, "wiI7pd").text
                star_element = r.find_element(By.CLASS_NAME, "kvMYJc")
                star_rating = star_element.get_attribute("aria-label") if star_element else "N/A"
                date = r.find_element(By.CLASS_NAME, "rsqaWe").text

                all_reviews.append({
                    "store_name": store,
                    "reviewer_name": reviewer,
                    "review_text": review_text,
                    "star_rating": star_rating,
                    "review_date": date
                })

            except Exception as e:
                print("Error reading review:", e)

    except Exception as e:
        print(f"Could not open reviews for {store}: {e}")

# Close the browser
driver.quit()

# Save to CSV
df = pd.DataFrame(all_reviews)
df.to_csv("reviews.csv", index=False)
print("✅ Done! Saved to reviews.csv")
