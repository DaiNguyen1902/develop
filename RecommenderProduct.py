import MySQLdb as mysql
import pandas as pd
import numpy as np
matrix_bought_filter = pd.read_csv('matrix_bought_filter.csv', index_col='customerId')
user_neighbors_filter = pd.read_csv('user_neighbors_filter.csv', index_col='customerId')
user_position_neighbors_filter = pd.read_csv('user_position_neighbors_filter.csv', index_col='customerId')
user_neighbors_filter_reset_index = user_neighbors_filter.reset_index()
list_product_recommend = pd.DataFrame(index=user_neighbors_filter_reset_index.index, columns=['customerId','item_recommend'])
def get_user_neighbors_filter(user_id):
    return user_neighbors_filter.iloc[user_id,:]
def get_list_item_bought(user_id):
    list_item_bought = []
    for i in range(0,len(matrix_bought_filter.columns)):
        if matrix_bought_filter.iloc[user_id,i]>0:
            list_item_bought.append(i)
    return list_item_bought
def get_array_item_not_similarly(arr1, arr2):
    return list(filter(lambda x:x not in  arr1, arr2))
def get_array_item_similarly(arr1, arr2):
    return list(filter(lambda x:x in  arr1, arr2))
def is_subset(root, target):
    arr_item_similarly = get_array_item_similarly(root, target)
    if(len(arr_item_similarly) == len(root)):
        return True
    return False
def get_list_item_recommend(user_id):
    number = 0
    list_all_item = []
    list_array_item_equal = []
    str_item_recommend = "|"
    list_item_target = get_list_item_bought(user_id)
    for i in range(0,len(user_neighbors_filter.columns)):
        list_item_root = get_list_item_bought(user_position_neighbors_filter.iloc[user_id, i])
        if(is_subset(list_item_root, list_item_target) == False):
            list_array_item_equal.append(get_array_item_not_similarly(list_item_target, list_item_root))
            number += 1
            if(number == 5):
                break
    for i in range(0, number):
        list_all_item += list_array_item_equal[i]
    list_all_item_unique = list(set(list_all_item))
    df_list_item_count = pd.DataFrame()
    df_list_item_count['productId'] = list_all_item_unique
    df_list_item_count['count']=0
    for i in range(0, len(df_list_item_count.index)):
        df_list_item_count.loc[i, 'count'] = list_all_item.count(df_list_item_count.loc[i,'productId'])
    df_list_item_count = df_list_item_count.sort_values(by='count', ascending=False).reset_index()
    for i in range(0,3):
        str_item_recommend = str_item_recommend + str(df_list_item_count.loc[i,'productId']) + '|'
    return str_item_recommend
def db_create_list_product_recommend():
    for i in range(0, len(user_neighbors_filter_reset_index.index)):
        list_product_recommend.loc[i, 'customerId'] = user_neighbors_filter_reset_index.loc[i,'customerId']
        list_product_recommend.loc[i, 'item_recommend'] = get_list_item_recommend(i)
        print(str(i*100/len(user_neighbors_filter_reset_index)) + "%")
db_create_list_product_recommend()
list_product_recommend.to_csv('list_product_recommend_filter.csv')
print(list_product_recommend)