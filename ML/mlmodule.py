import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

#defining columns to choose
colnames = ['timestamp','location-long','location-lat','visible']

# loading dataself.df.dropna(axis=0)
df = pd.read_csv('~/Desktop/everything nice/Programming/hackathon/SpaceApps2017/submission/samplesubs/cummulative.csv')
#print df
print df.head()
df.dropna(axis=0)

#creating matrix X and target vector y
X = df.as_matrix(columns=['location-long','location-lat','timestamp'])
y = df.as_matrix(columns=['visible'])

# splitting into train and test 
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.33,random_state=42)

#instantiate learning model(k=3)
knn = KNeighborsClassifier(n_neighbors=3)

#fitting the model
knn.fit(X_train,y_train)

#predict the response
pred = knn.predict(X_test)

#evaluate accuracy
print accuracy_score(y_test,pred)

print knn.predict([-6,38.29,0])
print knn.predict([-6,38.97,3])
print knn.predict([-6,38.8,3])
print knn.predict([-6,38.97,0])
print knn.predict([-34,151,4])
