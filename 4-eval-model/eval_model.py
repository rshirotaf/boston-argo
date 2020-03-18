import sys
import argparse
import numpy as np 
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def parse_args():
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
        "--split_path",  # name on the CLI - drop the `--` for positional/required parameters
        default=None,  # default if nothing is provided
        )
    CLI.add_argument(
        "--trained_model_path",  # name on the CLI - drop the `--` for positional/required parameters
        default=None,  # default if nothing is provided
        )
    CLI.add_argument(
        "--output_path",
         default='/tmp/output.pickle',
        )
    return CLI.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(args)

    split_path = args.split_path
    trained_model_path = args.trained_model_path
    
    X_train, X_test, Y_train, Y_test = [None, None, None, None]
    if not split_path is None:
        with open(split_path, 'rb') as file:
             X_train, X_test, Y_train, Y_test = pickle.load(file)

    trained_model = None
    if not trained_model_path is None:
        with open(trained_model_path, 'rb') as file:
             trained_model = pickle.load(file)

    y_train_predict = trained_model.predict(X_train)
    rmse = (np.sqrt(mean_squared_error(Y_train, y_train_predict)))

    print("The model performance for training set")
    print("--------------------------------------")
    print('RMSE is {}'.format(rmse))

    print("\n")

    # model evaluation for testing set
    y_test_predict = trained_model.predict(X_test)
    rmse = (np.sqrt(mean_squared_error(Y_test, y_test_predict)))

    print("The model performance for testing set")
    print("--------------------------------------")
    print('RMSE is {}'.format(rmse))
