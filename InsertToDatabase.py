import MySQLdb as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  passwd="",
  db="doantn_db"
)
mycursor = mydb.cursor()

import pandas as pd
import numpy as np

list_product_recommend_filter = pd.read_csv('list_product_recommend_filter.csv')
list_product_recommend_filter = list_product_recommend_filter.drop('Unnamed: 0',1)
print(list_product_recommend_filter)

def db_create_list_product_recommend():
    for i in range (0, len(list_product_recommend_filter)):
        '''
            Insert list item recommend for each user into database
        '''
        mycursor.execute("INSERT INTO item_recommends(user_id, item_recommend) values(" + str(list_product_recommend_filter.loc[i,'customerId']) + ", '" + list_product_recommend_filter.loc[i,'item_recommend'] + "')");
        mydb.commit()

        '''
            Insert info user(user_id, email, password) into database
        '''
        mycursor.execute("INSERT INTO users(id,email,password,login_times) values(" + str(list_product_recommend_filter.loc[i,'customerId']) + ", 'user" + str(list_product_recommend_filter.loc[i,'customerId']) + "@gmail.com', '$2y$10$ZkKFroXitmQY/PHlwwPBnOYxv9yODbQ/WB1CbN.bOWCTJGVRlsYx.',1)")
        mydb.commit()
db_create_list_product_recommend()