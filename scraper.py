import os
import random
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def scrape_product_list(search_url, num_pages=5, proxies=None):
    # Create the 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data' directory")

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    product_data = []

    for page in range(1, num_pages + 1):
        # Modify the URL to paginate
        paginated_url = f"{search_url}&page={page}"
        print(f"Scraping page {page}: {paginated_url}")

        # Retry logic in case of connection issues
        for attempt in range(3):  # Retry up to 3 times
            try:
                # Send a GET request to fetch the search page
                response = requests.get(paginated_url, headers=headers, proxies=proxies, timeout=10)
                print(f"HTTP Request Status Code: {response.status_code}")

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Debug: Print the first 500 characters of the page to check its structure
                    print(soup.prettify()[:500])

                    # Find all product containers on the page
                    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
                    print(f"Number of product containers found on page {page}: {len(product_containers)}")

                    # If no products found, stop scraping further pages
                    if len(product_containers) == 0:
                        print("No more products found. Exiting pagination.")
                        return product_data

                    # Iterate over each product container and extract the relevant details
                    for product in product_containers:
                        try:
                            title = product.h2.get_text(strip=True) if product.h2 else 'N/A'
                            link = f"https://www.amazon.co.uk{product.h2.a['href']}" if product.h2 and product.h2.a else 'N/A'
                            price = product.find('span', 'a-price-whole').get_text(strip=True) if product.find('span', 'a-price-whole') else 'N/A'

                            # Debug: Print extracted data for each product
                            print(f"Product Title: {title}, Price: {price}, Link: {link}")

                            # Append the data to the product list
                            product_data.append([title, link, price])
                        except AttributeError as e:
                            print(f"Failed to extract product details: {e}")
                            continue

                    # Sleep with a random delay to avoid getting blocked
                    time.sleep(random.uniform(1.5, 3.5))
                    break  # Break out of retry loop if successful

                else:
                    print(f"Failed to retrieve data from {paginated_url}. Status code: {response.status_code}")
                    break  # Stop retrying if we get a bad status code

            except (RequestException, Exception) as e:
                print(f"Error on attempt {attempt + 1}: {e}")
                if attempt == 2:  # If max retries reached, stop retrying
                    print("Max retries reached. Skipping this page.")
                else:
                    # Wait before retrying
                    time.sleep(random.uniform(2, 5))

    # Debug: Print the number of products collected
    print(f"Total number of products collected: {len(product_data)}")

    # If product data was collected, save it to a CSV file
    if product_data:
        product_df = pd.DataFrame(product_data, columns=["Product Name", "URL", "Price"])
        try:
            product_df.to_csv("data/product_list.csv", index=False)
            print(f"Saved {len(product_data)} products to 'data/product_list.csv'.")
        except Exception as e:
            print(f"Failed to save file. Error: {e}")
    else:
        print("No product data to save.")

    return product_data

# Example usage
if __name__ == "__main__":
    search_url = 'https://www.amazon.co.uk/s?k=baby+products'
    proxies = None  # Optional, remove or replace with your proxy settings if needed
    products = scrape_product_list(search_url, num_pages=5, proxies=proxies)
    
    if products is not None and len(products) > 0:
        print("Scraping completed successfully.")
    else:
        print("No products scraped.")
