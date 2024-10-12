import pandas as pd
import os

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"File {file_path} not found.")
        return None

def basic_statistics(df):
    print("Basic Statistics of the Scraped Data:")
    print(f"Total number of products: {len(df)}")
    print(f"Average Price: {df['Price'].replace('N/A', 0).astype(float).mean():.2f}")
    print(f"Minimum Price: {df['Price'].replace('N/A', 0).astype(float).min():.2f}")
    print(f"Maximum Price: {df['Price'].replace('N/A', 0).astype(float).max():.2f}")
    
    # Additional insights
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    print("Products priced above 50:")
    print(df[df['Price'] > 50])

def price_distribution(df):
    import matplotlib.pyplot as plt
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Plot distribution of prices
    plt.figure(figsize=(10, 6))
    df['Price'].dropna().plot(kind='hist', bins=20, color='blue', edgecolor='black')
    plt.title('Price Distribution of Scraped Products')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def main():
    # Load the data
    df = load_data('data/product_list.csv')
    
    if df is not None:
        # Perform basic statistics
        basic_statistics(df)
        
        # Generate visualizations
        price_distribution(df)

if __name__ == "__main__":
    main()
