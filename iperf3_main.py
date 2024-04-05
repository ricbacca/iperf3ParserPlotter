import sys
import matplotlib.pyplot as plt
import pandas as pd
from iperf3_data_parser import iperf3_dataParser

def correct_dataframe(df: pd.DataFrame, percentuale):
    means = df.mean()
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x if abs(x - means[col]) <= percentuale * means[col] else means[col])
    return df

def plot(df: pd.DataFrame, png_name, axis_names):
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.xlabel(axis_names[0])
    plt.ylabel(axis_names[1])
    plt.ylim(0, 4500)

    for col in df.columns:
        plt.plot(df.index.values, df[col], label=col)

    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    plt.savefig(png_name)    
    plt.show()   

        
if __name__ == "__main__":
    s = iperf3_dataParser()
    (foldername, output, plotFiles, axisNames, percentage) = s.parseOptions(sys.argv[1:])
    plotFiles=s.get_plotFiles(foldername, plotFiles)
    if len(plotFiles) > 0:
        dataset: pd.DataFrame = s.get_dataset(plotFiles, foldername)
    csv_corrected_dataset = correct_dataframe(dataset, percentage*0.01)
    plot(csv_corrected_dataset, output+".png", axisNames)                             