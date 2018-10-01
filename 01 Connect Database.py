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
results = conn.execute('select * from product').fetchall()
mydata= pd.DataFrame(results)

print(mydata)

