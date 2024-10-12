import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

# Load the data
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"File {file_path} not found.")
        return None

# Create the Dash app
app = dash.Dash(__name__)

# Load product data
df = load_data('data/product_list.csv')

# Clean up the data for plotting
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Create visualizations
def create_dashboard(df):
    # Scatter plot of product prices
    fig = px.scatter(df, x='Product Name', y='Price', title='Price of Products',
                    labels={'Product Name': 'Product', 'Price': 'Price (in £)'})
    
    # Create the app layout
    app.layout = html.Div([
        html.H1("Product Price Dashboard"),
        
        # Scatter plot
        dcc.Graph(
            id='price-scatter-plot',
            figure=fig
        ),
        
        # Histogram of product prices
        dcc.Graph(
            id='price-histogram',
            figure=px.histogram(df.dropna(), x='Price', nbins=20, title='Price Distribution of Products')
        )
    ])

# Start the dashboard
if df is not None:
    create_dashboard(df)
    app.run_server(debug=True)
else:
    print("No data to display in dashboard.")
