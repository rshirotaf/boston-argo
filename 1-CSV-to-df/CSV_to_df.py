import sys
import pandas as pd 
import pickle
import argparse


def parse_args():
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
        "--csv_path",  # name on the CLI - drop the `--` for positional/required parameters
        default=None,  # default if nothing is provided
        )
    CLI.add_argument(
        "--output_path",
         default='tmp/tmp_df.pickle',
        )
    return CLI.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print ("This is the name of the script: ", sys.argv[0])
    print ("Number of arguments: ", len(sys.argv))
    print ("The arguments are: " , str(sys.argv))
    print(args)

    csv_path = args.csv_path
    output_path = args.output_path

    if not csv_path is None:
        boston = pd.read_csv(csv_path, header = 0)
        print("\n**Header**")
        print(boston.head())

        print("\n**Any Missing Dataset**")
        print(boston.isnull().sum())
        
        with open(output_path, 'wb') as file:
          pickle.dump(boston, file)