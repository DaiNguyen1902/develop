import MySQLdb as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  passwd="123456",
  db="aseaspie_db"
)
mycursor = mydb.cursor()

from flask import Flask, render_template
import pandas as pd
import json
import numpy as np
matrix_bought = pd.read_csv('matrix_bought.csv', index_col='customerId')
user_neighbor = pd.read_csv('user_neighbors.csv', index_col='customerId')
user_position_neighbor = pd.read_csv('user_position_neighbors.csv', index_col='customerId')
user_neighbor_reset_index = user_neighbor.reset_index()
matrix_bought = matrix_bought[:3000]
list_product_recommend = pd.DataFrame(index=user_neighbor_reset_index.index, columns=['customerId','item_recommend'])
def get_user_neighbor(user_id):
    return user_neighbor.iloc[user_id,:]
def get_list_item_bought(user_id):
    list_item_bought = []
    for i in range(0,len(matrix_bought.columns)):
        if matrix_bought.iloc[user_id,i]>0:
            list_item_bought.append(i)
    return list_item_bought
def get_list_item_recommend(list_item_root,user_id):
    list_item_recommend = []
    str_item_recommend = '|'
    for i in range(0,len(user_neighbor.columns)):
        # list_item_user_similarly_bought = get_list_item_bought(user_neighbor.iloc[user_id, i])
        list_item_user_similarly_bought = get_list_item_bought(user_position_neighbor.iloc[user_id,i])
        list_item_not_in_list_item_user_similarly_bought = list(filter(lambda x:x not in  list_item_root,list_item_user_similarly_bought))
        list_item_not_in_list_item_recommend = list(filter(lambda x:x not in  list_item_recommend,list_item_not_in_list_item_user_similarly_bought))
        list_item_recommend= list_item_recommend+list_item_not_in_list_item_recommend
        if len(list_item_recommend) >= 20:
            break
    for i in range(0, len(list_item_recommend[:20])):
        str_item_recommend = str_item_recommend + str(list_item_recommend[i]) + '|'
    return str_item_recommend
def db_create_list_product_recommend():
    for i in range(0, len(user_neighbor_reset_index.index)):
        # list_item_root = get_list_item_bought(user_neighbor_reset_index.loc[i,'customerId'])
        list_item_root = get_list_item_bought(i)
        # list_item_recommend = get_list_item_recommend(list_item_root,user_neighbor_reset_index.loc[i,'customerId'])
        list_item_recommend = get_list_item_recommend(list_item_root, i)
        list_product_recommend.loc[i, 'item_recommend'] = list_item_recommend
        list_product_recommend.loc[i, 'customerId'] = user_neighbor_reset_index.loc[i,'customerId']
        print('user'+ str(user_neighbor_reset_index.loc[i,'customerId'])+': '+list_item_recommend)
        mycursor.execute("INSERT INTO item_recommends(user_id, item_recommend) values(" + str(user_neighbor_reset_index.loc[i,'customerId']) + ", '" + list_item_recommend + "')");
        mydb.commit()
db_create_list_product_recommend()
list_product_recommend.to_csv('list_product_recommend.csv')

