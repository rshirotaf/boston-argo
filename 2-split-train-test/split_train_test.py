##python3 split_train_test.py --df_path data/df.pickle --list_features lstat rm --rand_state 5 --test_size 0.2 --output_path /data/train_test_set.pickle --target medv

import sys
import argparse
import pandas as pd 
import numpy as np 
import pickle
from sklearn.model_selection import train_test_split

def parse_args():
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
        "--df_path",  # name on the CLI - drop the `--` for positional/required parameters
        default=None,  # default if nothing is provided
        )
    CLI.add_argument(
        "--list_features",
        nargs="*",
        default=[],
        )
    CLI.add_argument(
        "--output_path",
         default='/tmp/output.pickle',
        )
    CLI.add_argument(
        "--test_size",
        type=float,
        default=0.2,
        )
    CLI.add_argument(
        "--rand_state",
        type=int,
        default=5,
        )
    CLI.add_argument(
        "--target",
        default=None,
        )
    return CLI.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(args)

    df_path = args.df_path
    features = args.list_features
    target = args.target
    test_size = args.test_size
    rand_state = args.rand_state
    output_path = args.output_path

    X = None
    Y = None
        
    if not df_path is None:
        print(df_path)
        with open(df_path, 'rb') as file:
            boston = pickle.load(file)
            X = pd.DataFrame(boston[features].values, columns = features)
            Y = boston[target]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = test_size, random_state=rand_state)
    print(X_train.shape)
    print(X_test.shape)
    print(Y_train.shape)
    print(Y_test.shape)
    
    with open(output_path, 'wb') as file:
        pickle.dump([X_train, X_test, Y_train, Y_test], file)