import pandas as pd
import numpy as np
matrix_bought = pd.read_csv('matrix_bought.csv', index_col='customerId')
user_neighbor = pd.read_csv('user_neighbors.csv', index_col='customerId')
user_id = 2999
print(matrix_bought[:3000])
def get_user_neighbor(user_id):
    return user_neighbor.iloc[user_id,:]
def get_list_item_bought(user_id):
    list_item_bought = []
    for i in range(0,len(matrix_bought.columns)):
        if matrix_bought.iloc[user_id,i]>0:
            list_item_bought.append(i)
    return list_item_bought
def get_list_item_recommend(user_id):
    list_item_recommend = []
    for i in range(0,len(user_neighbor.columns)):
        list_item_user_similarly_bought = get_list_item_bought(user_neighbor.iloc[user_id,i])
        list_item_not_in_list_item_user_similarly_bought = list(filter(lambda x:x not in  list_item_root,list_item_user_similarly_bought))
        list_item_not_in_list_item_recommend = list(filter(lambda x:x not in  list_item_recommend,list_item_not_in_list_item_user_similarly_bought))
        list_item_recommend= list_item_recommend+list_item_not_in_list_item_recommend
        if len(list_item_recommend)>=20:
            return list_item_recommend[:20]
    if len(list_item_recommend)>0:
        return list_item_recommend
list_item_root = get_list_item_bought(user_id)
print(list_item_root)
print(get_list_item_recommend(user_id))
