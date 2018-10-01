import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def setting_connect(MYSQL_USER,MYSQL_PASSWORD,MYSQL_HOST_IP,MYSQL_PORT,MYSQL_DATABASE):
    engine=create_engine('mysql+mysqlconnector://'+MYSQL_USER+':'+MYSQL_PASSWORD+'/'+MYSQL_DATABASE+'?host='+MYSQL_HOST_IP+'?port='+MYSQL_PORT)
    return engine.connect()

conn = setting_connect('root','mavacaga@localhost','localhost','3306','latihanujian')

results = conn.execute("SELECT p.id as productid,p.nama as namaproduct, "
                       +"c.nama as namacategory,v.nama as namavendor,p.price, "
                       +"p.totalStock,v.jointYear,p.stockSekarang "
                       +"FROM product p "
                       +"JOIN vendor v ON v.id = p.vendorid "
                       +"JOIN category c ON c.id = p.categoryid "
                       +"ORDER by p.id").fetchall()
mydata= pd.DataFrame(results)
mydata.columns = results[0].keys()
print(mydata.head())
