import pandas as pd
import random
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# 1. Generate Product Details (200 records)
product_categories = ['Printers', 'Laptops', 'Desktops', 'Accessories']
product_names = [
    'Laser Printer XYZ 2000', 'HP Deskjet 3750 Printer', 'Canon PIXMA TS3320',
    'Dell Inspiron 15 5000 Laptop', 'HP Pavilion 14 Laptop', 'Logitech Wireless Mouse',
    'HP Pavilion Home Desktop', 'Acer Aspire 5 Desktop', 'Lenovo ThinkPad L15',
    'HP LaserJet Pro MFP M428fdw', 'Samsung 32" Curved Monitor', 'Epson EcoTank ET-2720 Printer'
]

brands = ['HP', 'Canon', 'Epson', 'Dell', 'Acer', 'Lenovo', 'Logitech', 'Samsung']
prices = [99.99, 199.99, 150.00, 549.99, 749.99, 29.99, 599.99, 799.99, 899.99, 199.00, 179.99]
ratings = [round(random.uniform(3.0, 5.0), 1) for _ in range(200)]

product_details = {
    'product_id': [f'P{i+1}' for i in range(200)],
    'product_name': random.choices(product_names, k=200),
    'category': random.choices(product_categories, k=200),
    'brand': random.choices(brands, k=200),
    'price': random.choices(prices, k=200),
    'rating': ratings
}

df_product_details = pd.DataFrame(product_details)

# Save Product Details as CSV
df_product_details.to_csv('product_details.csv', index=False)

# 2. Generate User Product Ratings (4000 records)
user_ids = [f'U{i+1}' for i in range(50)]  # 50 unique users
product_ids = df_product_details['product_id'].tolist()  # 200 unique products

user_product_ratings = {
    'user_id': random.choices(user_ids, k=4000),
    'product_id': random.choices(product_ids, k=4000),
    'rating': random.choices([1, 2, 3, 4, 5], k=4000),
    'timestamp': [f'2023-10-{random.randint(1, 31):02d} {random.randint(10, 23)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}' for _ in range(4000)]
}

df_user_product_ratings = pd.DataFrame(user_product_ratings)

# Save User Product Ratings as CSV
df_user_product_ratings.to_csv('user_product_ratings.csv', index=False)

# 3. Generate User Details (50 records)
ages = random.choices(range(18, 70), k=50)  # Age between 18 and 70
genders = random.choices(['Male', 'Female', 'Other'], k=50)
locations = random.choices(['New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Houston'], k=50)
membership_levels = random.choices(['Basic', 'Premium', 'VIP'], k=50)

user_details = {
    'user_id': user_ids,
    'age': ages,
    'gender': genders,
    'location': locations,
    'membership_level': membership_levels
}

df_user_details = pd.DataFrame(user_details)

# Save User Details as CSV
df_user_details.to_csv('user_details.csv', index=False)

print("CSV files have been created successfully!")
