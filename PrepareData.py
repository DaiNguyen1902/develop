import pandas as pd
import numpy as np

import sys
sys.path.append("..")
customers = pd.read_csv('recommend_1.csv')
transactions = pd.read_csv('trx_data.csv')
transactions['products'] = transactions['products'].apply(lambda x: [int(i) for i in x.split('|')])
print(transactions.head(15))
transactions.to_csv('list_item_has_been_purchased.csv')
data = pd.melt(transactions.set_index('customerId')['products'].apply(pd.Series).reset_index(),
             id_vars=['customerId'],
             value_name='products').dropna().drop(['variable'], axis=1).groupby(['customerId', 'products']).agg({'products': 'count'}).rename(columns={'products': 'purchase_count'}).reset_index().rename(columns={'products': 'productId'})
data['productId'] = data['productId'].astype(np.int64)
print(data)
data.to_csv('purchase_count.csv')


