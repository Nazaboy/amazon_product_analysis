import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def scrape_product_list(search_url, num_pages=5):
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

        # Send a GET request to fetch the search page
        response = requests.get(paginated_url, headers=headers)
        print(f"HTTP Request Status Code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all product containers on the page
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            print(f"Number of product containers found on page {page}: {len(product_containers)}")

            # If no products found, likely hit a limit, stop scraping further pages
            if len(product_containers) == 0:
                print("No more products found. Exiting pagination.")
                break

            # Iterate over each product container and extract the relevant details
            for product in product_containers:
                title = product.h2.get_text(strip=True)

                # Extract the product URL (partial link, so we need to add the base URL)
                link = f"https://www.amazon.co.uk{product.h2.a['href']}"

                # Extract the price (check if price is available, otherwise N/A)
                price = product.find('span', 'a-price-whole').get_text(strip=True) if product.find('span', 'a-price-whole') else 'N/A'

                # Append the data to the product list
                product_data.append([title, link, price])

            # Sleep between requests to avoid being blocked
            time.sleep(2)

        else:
            print(f"Failed to retrieve data from {paginated_url}. Status code: {response.status_code}")
            break

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
    products = scrape_product_list(search_url, num_pages=5)  # Change num_pages as needed
    
    if products is not None and len(products) > 0:
        print("Scraping completed successfully.")
    else:
        print("No products scraped.")
