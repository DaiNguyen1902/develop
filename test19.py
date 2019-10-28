import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split
matrix_bought = pd.read_csv('matrix_bought.csv', index_col='customerId')
matrix_bought = matrix_bought[:3000]
matrix_bought_reset_index = matrix_bought.reset_index()
test_data = matrix_bought_reset_index[:100]
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

def get_list_item_recommend(list_item_root,user_id): # lay danh san pham goi y cho user_id
    list_item_recommend = []
    str_item_recommend = '|'
    for i in range(0,len(user_neighbors.columns)):
        # list_item_user_similarly_bought = get_list_item_bought(user_neighbor.iloc[user_id, i])
        list_item_user_similarly_bought = get_list_item_bought(user_position_neighbors.iloc[user_id,i])
        list_item_not_in_list_item_user_similarly_bought = list(filter(lambda x:x not in  list_item_root,list_item_user_similarly_bought))
        list_item_not_in_list_item_recommend = list(filter(lambda x:x not in  list_item_recommend,list_item_not_in_list_item_user_similarly_bought))
        list_item_recommend= list_item_recommend+list_item_not_in_list_item_recommend
        if len(list_item_recommend) >= 20:
            break
    for i in range(0, len(list_item_recommend[:20])):
        str_item_recommend = str_item_recommend + str(list_item_recommend[i]) + '|'
    return str_item_recommend

def set_matrix_bought_from_test_data(): # Dat lai ma tran mua tu tap du lieu kiem tra
    for i in range(0, len(test_data.index)):
        arr_item_bought = get_list_item_bought(i)
        item_remove = arr_item_bought.pop()
        item_remove_data.loc[i,'item_remove'] = item_remove
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

accuracy = 0
# list_product_recommend_test = pd.read_csv('list_product_recommend_test.csv')
# list_product_recommend_test = list_product_recommend_test.drop('Unnamed: 0', 1)
# list_product_recommend_test = list_product_recommend_test.reset_index()
list_product_recommend_test = pd.DataFrame(index=user_neighbor_reset_index.index, columns=['customerId','item_recommend'])

def db_create_list_product_recommend():
    for i in range(0, len(user_neighbor_reset_index.index)):
        list_item_root = get_list_item_bought(i)
        list_item_recommend = get_list_item_recommend(list_item_root, i)
        list_product_recommend_test.loc[i, 'item_recommend'] = list_item_recommend
        list_product_recommend_test.loc[i, 'customerId'] = user_neighbor_reset_index.loc[i,'customerId']
        print('user'+ str(user_neighbor_reset_index.loc[i,'customerId'])+': '+list_item_recommend)
db_create_list_product_recommend()
list_product_recommend_test.to_csv('list_product_recommend_test.csv')
for i in range(0, len(test_data.index)):
    list_item_root = get_list_item_bought(i)
    print(list_item_root)
    list_item_recommend = get_list_item_recommend(list_item_root, i)
    print(item_remove_data.loc[i,'item_remove'])
    print(list_item_recommend)
    if ("|"+str(item_remove_data.loc[i,'item_remove'])+"|") in str(list_product_recommend_test.loc[i, 'item_recommend']):
        print('position:' + str(i))
        accuracy = accuracy+1/len(test_data.index)
print(accuracy)