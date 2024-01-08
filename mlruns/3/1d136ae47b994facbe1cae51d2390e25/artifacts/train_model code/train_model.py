from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd
 
df = pd.read_csv('/home/angry/mlops_3/datasets/data_train.csv', header=None)
df.columns = ['id', 'counts']
 
model = LinearRegression()
model.fit(df['id'].values.reshape(-1,1), df['counts'])
 
with open('/home/angry/mlops_3/models/data.pickle', 'wb') as f:
    pickle.dump(model, f)
