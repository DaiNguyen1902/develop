import pandas as pd
import numpy as np

data_user_base_frame_filter = pd.read_csv('data_user_base_frame_filter.csv', index_col='customerId')
data_user_base_frame_filter_reset_index = data_user_base_frame_filter.reset_index()
print(data_user_base_frame_filter)
data = np.array(data_user_base_frame_filter)
list_customer_id = data_user_base_frame_filter.index # customer id column
index = np.argsort(data, axis=-1) # sort index
def get_sorted_index(customer_id):
    customer_id_index = np.where(list_customer_id == customer_id)[0][0] # get customer id from list_id
    return list_customer_id[index[customer_id_index][1:101]]
def get_sorted_position_index(customer_id):
    customer_id_index = np.where(list_customer_id == customer_id)[0][0] # get customer id from list_id
    return index[customer_id_index][1:101]
user_neighbors_filter = pd.DataFrame(index=data_user_base_frame_filter.index, columns=range(0,100))
user_position_neighbors_filter = pd.DataFrame(index=data_user_base_frame_filter.index, columns=range(0, 100))
for i in range(0, len(data_user_base_frame_filter.columns)):
    user_neighbors_filter.iloc[i,:100] = get_sorted_index(data_user_base_frame_filter_reset_index.loc[i,'customerId'])
for i in range(0, len(data_user_base_frame_filter.columns)):
    user_position_neighbors_filter.iloc[i,:100] = get_sorted_position_index(data_user_base_frame_filter_reset_index.loc[i,'customerId'])
user_neighbors_filter.to_csv('user_neighbors_filter.csv')
print(user_neighbors_filter)
user_position_neighbors_filter.to_csv('user_position_neighbors_filter.csv')
print(user_position_neighbors_filter)
