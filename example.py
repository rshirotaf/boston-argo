## Raw code is from https://towardsdatascience.com/linear-regression-on-boston-housing-dataset-f409b7e4a155

import numpy as np
import matplotlib.pyplot as plt 

import pandas as pd  
import seaborn as sns 

#matplotlib inline


##Function Load_CSV (???)
##Input: path_to_data, csv_filename, path_to_output, pickle_data_filename
##Output: pickle_dict_data
##Extra: I will try to code a function to load data from CSV in my MiniIO.
## CSV download: https://www.kaggle.com/prasadperera/the-boston-housing-dataset
##with open('/full/path/to/file', 'wb') as f:
##  pickle.dump(object, f)
from sklearn.datasets import load_boston
boston_dataset = load_boston()
print("\n**Key**")
print(boston_dataset.keys())

boston = pd.DataFrame(boston_dataset.data, columns=boston_dataset.feature_names)
print("\n**Header**")
print(boston.head())

boston['MEDV'] = boston_dataset.target

print("\n**Any Missing Dataset**")
print(boston.isnull().sum())


##Function Draw_Hist
##Input: path_to_data, data, bins_size, path_to_output
##Output: Save image
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.distplot(boston['MEDV'], bins=30)
plt.show()


##Function Draw_Heatmap
##Input: path_to_data, dataframe, path_to_output
##Output: Save image
correlation_matrix = boston.corr().round(2)
# annot = True to print the values inside the square
sns.heatmap(data=correlation_matrix, annot=True)
plt.show()

plt.figure(figsize=(20, 5))


##Function Plot_Relationship
##Input: path_to_data, features, target, path_to_output
##Output: Save image
features = ['LSTAT', 'RM']
target = boston['MEDV']

for i, col in enumerate(features):
    plt.subplot(1, len(features) , i+1)
    x = boston[col]
    y = target
    plt.scatter(x, y, marker='o')
    plt.title(col)
    plt.xlabel(col)
    plt.ylabel('MEDV')
plt.show()


##Function Split_Train_Test
##Input: path_to_data, dataframe, feature, target, test_size, random_state, 
##  path_to_output, pickle_test_train_filename
##Output: pickle_test_train, which contains {X_train, X_test, Y_train, Y_test}
X = pd.DataFrame(np.c_[boston['LSTAT'], boston['RM']], columns = ['LSTAT','RM'])
Y = boston['MEDV']

from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=5)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)


##Function Train_Model
##Input: path_to_model, pickle_test_train_filename, path_to_output, pickle_model_filename
##Output: pickle_model, which contains {lin_model}
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

lin_model = LinearRegression()
lin_model.fit(X_train, Y_train)


##Function Eval_Model
##Input: path_to_model, pickle_test_train_filename, pickle_model_filename, path_to_output, result_filename
##Output: text file

# model evaluation for training set
y_train_predict = lin_model.predict(X_train)
rmse = (np.sqrt(mean_squared_error(Y_train, y_train_predict)))

print("The model performance for training set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))

print("\n")

# model evaluation for testing set
y_test_predict = lin_model.predict(X_test)
rmse = (np.sqrt(mean_squared_error(Y_test, y_test_predict)))

print("The model performance for testing set")
print("--------------------------------------")
print('RMSE is {}'.format(rmse))

