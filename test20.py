import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split

list_product_recommend = pd.read_csv('list_product_recommend.csv', index_col='customerId')
list_product_recommend = list_product_recommend.drop('Unnamed: 0', 1)
list_product_recommend = list_product_recommend.reset_index()
print(list_product_recommend.reset_index())