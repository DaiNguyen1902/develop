import pandas as pd
import numpy as np
pd_matrix = pd.read_csv('number_bought.csv', index_col="customerId")
print(pd_matrix.shape)
print(pd_matrix.info())

matrix_bought = pd.DataFrame(index=pd_matrix.index, columns= pd_matrix.columns)
for i in range(0, len(matrix_bought.index)):
    for j in range(0, len(matrix_bought.columns)):
        if(pd_matrix.iloc[i,j] > 0):
            matrix_bought.iloc[i,j] = 1
        else:
            matrix_bought.iloc[i,j] = 0
# pd_matrix.reset_index()
matrix_bought.to_csv('matrix_bought.csv', index='customerId')
print(matrix_bought)
