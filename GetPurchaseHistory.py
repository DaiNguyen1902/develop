import pandas as pd
import numpy as np

import sys


def get_array_item_not_similarly(arr1, arr2):
  return list(filter(lambda x: x not in arr1, arr2))

def get_history_bought(user_id):
  list_item_bought = transactions[transactions.customerId == user_id]
  list_item_bought = list_item_bought.sort_values(by='index', ascending=True).reset_index()
  if(len(list_item_bought) == 0):
    return []
  history_bought = []
  for i in range(0, len(list_item_bought)):
    history_bought += get_array_item_not_similarly(history_bought, set(list_item_bought.loc[i, 'products']))
  history_bought = str(history_bought)
  history_bought = history_bought.replace('[','')
  history_bought = history_bought.replace(']', '')
  history_bought = history_bought.replace(', ', '|')
  return  str(history_bought)
sys.path.append("..")
list_product_recommend_filter = pd.read_csv('list_product_recommend_filter.csv')
list_product_recommend_filter = list_product_recommend_filter.drop('Unnamed: 0', 1)
transactions = pd.read_csv('trx_data.csv')
transactions['products'] = transactions['products'].apply(lambda x: [int(i) for i in x.split('|')])
transactions = transactions.sort_values(by='customerId', ascending=True).reset_index()

len_list_product_recommend_filter = len(list_product_recommend_filter.index)
df_history_bought = pd.DataFrame(index=list_product_recommend_filter.index)
for i in range(0, len(df_history_bought.index)):
  df_history_bought.loc[i, 'customerId'] = list_product_recommend_filter.loc[i, 'customerId']
  df_history_bought.loc[i, 'item_bought'] = get_history_bought(list_product_recommend_filter.loc[i, 'customerId'])
  print(str(i*100/len_list_product_recommend_filter)+ "%")
df_history_bought['customerId'] = df_history_bought['customerId'].astype(int)
df_history_bought.to_csv('history_bought.csv')
print(df_history_bought)






