import sys
import matplotlib.pyplot as plt 
import pandas as pd  
import seaborn as sns
import pickle
import argparse

def parse_args():
    CLI= argparse.ArgumentParser()
    CLI.add_argument(
        "--df_path",  
        default=None,  
        )
    CLI.add_argument(
        "--save_img_path",
         default='/tmp/img.jpg',
        )
    CLI.add_argument(
        "--list_features",
        nargs="*",
        default=[],
        )
    CLI.add_argument(
        "--target",
        default=None,
        )
    CLI.add_argument(
        "--bins",
        type=int,
        default=10
        )
    CLI.add_argument(
        "--draw_type",
        choices=['hist', 'heatmap', 'plot'],
        default='hist'
        )
    return CLI.parse_args()

def plot_hist(data, bins, img_path):
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    tmp = sns.distplot(data, bins=bins)
    fig = tmp.get_figure()
    fig.savefig(img_path)
    plt.show()

def plot_heatmap(df, img_path):
    correlation_matrix = df.corr().round(2)
    # annot = True to print the values inside the square
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    tmp = sns.heatmap(data=correlation_matrix, annot=True)
    #plt.show()
    fig = tmp.get_figure()
    fig.savefig(img_path)

def plot_against(df, features, target, img_path):
    plt.figure(figsize=(20, 5))
    y = df[target]

    for i, col in enumerate(features):
        plt.subplot(1, len(features) , i+1)
        x = df[col]
        plt.scatter(x, y, marker='o')
        plt.title(col)
        plt.xlabel(col)
        plt.ylabel(target)
    plt.savefig(img_path)
    #plt.show()

if __name__ == '__main__':
    args = parse_args()
    print(args)

    df_path = args.df_path
    draw_type = args.draw_type
    features = args.list_features
    target = args.target
    bins = args.bins
    save_img_path = args.save_img_path

    df = None
            
    if not df_path is None:
        with open(df_path, 'rb') as file:
            df = pickle.load(file)

    if draw_type == 'hist':
        plot_hist(data=df[target], bins=bins, img_path=save_img_path)
    if draw_type == 'heatmap':
        plot_heatmap(df=df, img_path=save_img_path)
    if draw_type == 'plot':
        plot_against(df=df, features=features, target=target, 
                    img_path=save_img_path)

