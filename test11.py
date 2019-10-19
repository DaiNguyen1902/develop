import pandas as pd
import numpy as np

data_user_base_frame = pd.read_csv('data_user_base_frame.csv', index_col='customerId')
data_user_base_frame_reset_index = data_user_base_frame.reset_index()
print(data_user_base_frame_reset_index)
data = np.array(data_user_base_frame)
list_customer_id = data_user_base_frame.index # customer id column
index = np.argsort(data, axis=-1) # sort index
def get_sorted_index(customer_id):
    customer_id_index = np.where(list_customer_id == customer_id)[0][0] # get customer id from list_id
    return list_customer_id[index[customer_id_index]][1:21]
user_neighbors = pd.DataFrame(index=data_user_base_frame.index, columns=range(0,20))
for i in range(0, len(data_user_base_frame.columns)):
    user_neighbors.iloc[i,:20] = get_sorted_index(data_user_base_frame_reset_index.loc[i,'customerId'])
user_neighbors.to_csv('user_neighbors.csv')
print(user_neighbors)



