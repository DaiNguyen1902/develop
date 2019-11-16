import pandas as pd
import numpy as np

history_bought = pd.read_csv('history_bought.csv')
history_bought['item_bought'] = history_bought['item_bought'].apply(lambda x: [int(i) for i in x.split('|')])
history_bought = history_bought.drop('Unnamed: 0', 1)

from sklearn.metrics import pairwise_distances
matrix_bought = pd.read_csv('matrix_bought_filter.csv', index_col='customerId')
matrix_bought_reset_index = matrix_bought.reset_index()
test_data = matrix_bought_reset_index[:100]
print(test_data)
item_remove_data = pd.DataFrame(index=test_data.index, columns=['item_remove'])
def get_user_neighbor(user_id): # lay dang sach user_neighbors cua user_id
    return user_neighbors.iloc[user_id,:]
def get_list_item_bought(user_id): # lay danh sach cac san pham da mua cua user_id
    list_item_bought = []
    for i in range(0,len(matrix_bought.columns)):
        if matrix_bought.iloc[user_id,i]>0:
            list_item_bought.append(i)
    return list_item_bought
def get_sorted_index(customer_id): # tra ve danh sach cac user co khoang cach tang dan
    customer_id_index = np.where(list_customer_id == customer_id)[0][0] # get customer id from list_id
    return list_customer_id[index[customer_id_index][1:21]]
def get_sorted_position_index(customer_id): # tra ve danh sach index cua cac user co khoang cach tang dan
    customer_id_index = np.where(list_customer_id == customer_id)[0][0] # get customer id from list_id
    return index[customer_id_index][1:21]
def get_array_item_not_similarly(arr1, arr2):
  return list(filter(lambda x: x not in arr1, arr2))
def get_array_item_similarly(arr1, arr2):
  return list(filter(lambda x: x in arr1, arr2))
def is_subset(root, target):
    arr_item_similarly = get_array_item_similarly(root, target)
    if (len(arr_item_similarly) == len(root)):
      return True
    return False
def get_list_item_recommend(user_id):
  number = 0
  list_all_item = []
  list_array_item_equal = []
  str_item_recommend = "|"
  list_item_target = get_list_item_bought(user_id)
  for i in range(0, len(user_neighbors.columns)):
    list_item_root = get_list_item_bought(user_position_neighbors.iloc[user_id, i])
    if (is_subset(list_item_root, list_item_target) == False):
      list_array_item_equal.append(get_array_item_not_similarly(list_item_target, list_item_root))
      number += 1
      if (number == 5):
        break
  for i in range(0, number):
    list_all_item += list_array_item_equal[i]
  list_all_item_unique = list(set(list_all_item))
  df_list_item_count = pd.DataFrame()
  df_list_item_count['productId'] = list_all_item_unique
  df_list_item_count['count'] = 0
  for i in range(0, len(df_list_item_count.index)):
    df_list_item_count.loc[i, 'count'] = list_all_item.count(df_list_item_count.loc[i, 'productId'])
  df_list_item_count = df_list_item_count.sort_values(by='count', ascending=False).reset_index()
  for i in range(0, 5):
    str_item_recommend = str_item_recommend + str(df_list_item_count.loc[i, 'productId']) + '|'
  return str_item_recommend
def set_matrix_bought_from_test_data(): # Dat lai ma tran mua tu tap du lieu kiem tra
    for i in range(0, len(test_data.index)):
        arr_item_bought = history_bought.loc[i, 'item_bought']
        item_remove_data.loc[i, 'item_remove'] = []
        for j in range(0, 5):
          item_remove = arr_item_bought.pop()
          item_remove_data.loc[i,'item_remove'].append(item_remove)
          matrix_bought.iloc[i,item_remove] = 0
set_matrix_bought_from_test_data()
data_user_base_frame = pairwise_distances(matrix_bought, metric="euclidean") # Ma tran do tuong tu giua cac user
data_user_base_frame = pd.DataFrame(data_user_base_frame, index=matrix_bought.index, columns=matrix_bought.index)
data_user_base_frame_reset_index = data_user_base_frame.reset_index() # Dat lai index
data = np.array(data_user_base_frame)
list_customer_id = data_user_base_frame.index # customer id column
index = np.argsort(data, axis=-1) # sort index

user_neighbors = pd.DataFrame(index=data_user_base_frame.index, columns=range(0,20)) # Khai bao ma tran user_neighbors
user_position_neighbors = pd.DataFrame(index=data_user_base_frame.index, columns=range(0,20)) # Khai bao ma tran vi tri cua user_neighbors
for i in range(0, len(data_user_base_frame.columns)):
    user_neighbors.iloc[i,:20] = get_sorted_index(data_user_base_frame_reset_index.loc[i,'customerId'])
for i in range(0, len(data_user_base_frame.columns)):
    user_position_neighbors.iloc[i,:20] = get_sorted_position_index(data_user_base_frame_reset_index.loc[i,'customerId'])
user_neighbor_reset_index = user_neighbors.reset_index()

list_product_recommend = pd.DataFrame(index=user_neighbor_reset_index.index, columns=['customerId','item_recommend'])
def db_create_list_product_recommend():
  for i in range(0, len(user_neighbor_reset_index.index)):
    list_product_recommend.loc[i, 'customerId'] = user_neighbor_reset_index.loc[i, 'customerId']
    list_product_recommend.loc[i, 'item_recommend'] = get_list_item_recommend(i)
    print(str(i * 100 / len(user_neighbor_reset_index)) + "%")

db_create_list_product_recommend()
list_product_recommend.to_csv('list_product_recommend_test.csv')
item_remove_data.to_csv('list_item_test_remove.csv')
print(list_product_recommend)
accuracy = 0
recall = 0
precision = 0

for i in range (0, 100):
  for j in range (0, 5):
    if ("|"+str(item_remove_data.loc[i,'item_remove'][j])+"|") in str(list_product_recommend.loc[i, 'item_recommend']):
        print('position:' + str(i) + ',' + str(j))
        precision += 1/5
        recall += 1/3
print('recall mean: ' + str(recall/100))
print('precision mean: '+ str(precision/100))

# print(item_remove_data.loc[0,'item_remove'][1])