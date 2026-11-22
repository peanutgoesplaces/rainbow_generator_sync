from vision import retrieve_current_inventory, generate_weekly_sales_df
from database import conn
import pandas as pd
from datetime import date, datetime


current_inventory_df = retrieve_current_inventory()
weekly_sales_df = generate_weekly_sales_df()

today = date.today()
#Upload Current Inventory to Database

def insert_current_inventory(df):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO current_inventory
            (item_num, item, qoh, inventory_date)
            VALUES( %s, %s, %s, %s)
            ON CONFLICT (item_num)
            DO UPDATE SET
                item = EXCLUDED.item,
                qoh = EXCLUDED.qoh,
                inventory_date = EXCLUDED.inventory_date
            """, (
            row['item_num'],
            row['item'],
            row['qoh'],
            today
        ))

    conn.commit()
    print('upload complete')
    cursor.close()

