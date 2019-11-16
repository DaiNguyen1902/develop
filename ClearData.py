import pandas as pd

dataset = pd.read_csv('purchase_count.csv')
dataset = dataset.drop('Unnamed: 0', 1)
max_purchase_count = dataset['purchase_count'].max()
df_users = pd.DataFrame(dataset.groupby('customerId').size(), columns=['count'])
popular_user = list(set(df_users.query('count >= 10').index))

df_items = pd.DataFrame(dataset.groupby('productId').size(), columns=['count'])
popular_item = list(set(df_items.query('count >= 0').index))

users_filter = dataset.customerId.isin(popular_user).values
items_filter = dataset.productId.isin(popular_item).values

dataset_filter = dataset[users_filter & items_filter]
df_matrix = pd.pivot_table(dataset_filter, values='purchase_count', index='customerId', columns='productId').fillna(0)
print(df_matrix)
print(max_purchase_count)
for i in range (1,max_purchase_count+1):
    df_matrix = df_matrix.replace(i, 1)
print(df_matrix)
df_matrix = pd.DataFrame(df_matrix)
df_matrix.to_csv('matrix_bought_filter.csv')