import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text, Integer

# --- 1. DATABASE SETTINGS ---
DB_USER = 'root'
DB_PASS = 'YOUR_PASSWORD'  # <-- Tera password yahan set kar diya hai
DB_NAME = 'YOUR_DATABASE_NAME'

try:
    # Connection string
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}")
    print("✅ Connection Successful! MySQL se jud gaye hain.")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    exit()

# --- 2. DATA GENERATION ---
phones = [
    ('Apple', 'iPhone 15 Pro', 134900), ('Apple', 'iPhone 15', 79900),
    ('Apple', 'iPhone 14', 69900), ('Apple', 'iPhone 13', 59900),
    ('Samsung', 'S24 Ultra', 129900), ('Samsung', 'S23 FE', 54900),
    ('Samsung', 'A54 5G', 35000), ('Samsung', 'Z Fold 5', 154000)
]

stores = [
    (1, 'Pune - FC Road', 'Flagship'), (2, 'Mumbai - Colaba', 'Mall Store'),
    (3, 'Nagpur - Sitabuldi', 'Local Dealer'), (4, 'Nashik - City Center', 'Mall Store')
]

df_phones = pd.DataFrame([{'phone_id': i+1, 'brand': p[0], 'model_name': p[1], 'storage': '256GB', 'base_price': p[2]} for i, p in enumerate(phones)])
df_stores = pd.DataFrame([{'store_id': s[0], 'store_location': s[1], 'store_type': s[2]} for s in stores])

sales_data = []
start_date = datetime(2026, 1, 1)

for i in range(1200):
    p_idx = random.randint(0, len(phones)-1)
    phone = phones[p_idx]
    store = random.choice(stores)
    discount = round(random.uniform(2, 6), 2) if phone[0] == 'Apple' else round(random.uniform(8, 18), 2)
    qty = random.choice([1, 2])
    final_price = round((phone[2] * qty) * (1 - discount/100), 2)
    profit = round(final_price * (0.20 if phone[0] == 'Apple' else 0.15), 2)
    
    sales_data.append({
        'order_date': (start_date + timedelta(days=random.randint(0, 110))).strftime('%Y-%m-%d'),
        'phone_id': p_idx + 1,
        'store_id': store[0],
        'quantity': qty,
        'discount_percent': discount,
        'final_price': final_price,
        'profit_margin': profit
    })

df_sales = pd.DataFrame(sales_data)

# --- 3. PUSH TO SQL (The Clean Way) ---
print("⏳ Data load ho raha hai... Thoda wait karo.")

with engine.connect() as conn:
    # A. Pehle saare purane rishte (Foreign Keys) aur tables khatam karo
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    conn.execute(text("DROP TABLE IF EXISTS fact_sales;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_phones;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_stores;"))
    
    # B. Naye Tables create aur data insert karo
    df_phones.to_sql('dim_phones', con=conn, if_exists='replace', index=False, dtype={'phone_id': Integer})
    df_stores.to_sql('dim_stores', con=conn, if_exists='replace', index=False, dtype={'store_id': Integer})
    df_sales.to_sql('fact_sales', con=conn, if_exists='replace', index=False, dtype={'phone_id': Integer, 'store_id': Integer})
    
    # C. SQL CONSTRAINTS (Primary Keys aur Foreign Keys wapas lagao)
    print("🛠️ SQL rules set kar raha hoon...")
    conn.execute(text("ALTER TABLE dim_phones ADD PRIMARY KEY (phone_id);"))
    conn.execute(text("ALTER TABLE dim_stores ADD PRIMARY KEY (store_id);"))
    
    # order_id column aur primary key set karo
    conn.execute(text("ALTER TABLE fact_sales ADD COLUMN order_id INT AUTO_INCREMENT PRIMARY KEY FIRST;"))
    
    # Linking Foreign Keys
    conn.execute(text("ALTER TABLE fact_sales ADD CONSTRAINT fk_phone FOREIGN KEY (phone_id) REFERENCES dim_phones(phone_id);"))
    conn.execute(text("ALTER TABLE fact_sales ADD CONSTRAINT fk_store FOREIGN KEY (store_id) REFERENCES dim_stores(store_id);"))
    
    conn.commit()
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

print("-" * 45)
print("🚀 MISSION SUCCESS! 1,200 Records Loaded.")
print("Ab MySQL Workbench mein jaakar data check karo!")
print("-" * 45)