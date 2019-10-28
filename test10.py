import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean

dataset = pd.read_csv('matrix_bought.csv', index_col='customerId')
dataset = dataset[:8000]
data_user_base_frame = pairwise_distances(dataset, metric="euclidean")
data_user_base_frame = pd.DataFrame(data_user_base_frame, index=dataset.index, columns=dataset.index)
data_user_base_frame.to_csv('data_user_base_frame.csv')
print(data_user_base_frame)
