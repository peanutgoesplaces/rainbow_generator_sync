from vision import retrieve_current_inventory, generate_weekly_sales_df
from database import conn
import pandas as pd
from datetime import date, datetime, timedelta
from upload_to_database import insert_current_inventory

current_inventory_df = retrieve_current_inventory()
weekly_sales_df = generate_weekly_sales_df()
#print(current_inventory_df[current_inventory_df['dept'] == 'CIGARETTES'])
master_inventory  = pd.read_sql(
    "SELECT * FROM vision_master_list",
    conn
)



rainbow = current_inventory_df[
        (current_inventory_df['dept'] == 'CIGARETTES')
]

merged_df = master_inventory.merge(
    current_inventory_df[['item', 'qoh']],
    how='left',
    on=['item']

)



merged_df = merged_df.fillna(0)

merged_df = merged_df[['item_num', 'item', 'qoh']]


insert_current_inventory(merged_df)