#!../../../venv/bin/python3
import ast
import sys
import numpy as np


def analyse_pseudo_csv(filepath):
    """analyse colour sensor output from file at filepath"""
    data = list()
    output = dict()
    with open(filepath, 'r') as file:
        for line in file:
            # interpret each line as a list
            # extract color components
            r,g,b = ast.literal_eval(line.strip())
            sum_rgb = r+g+b
            # append normalised values
            data.append([r/sum_rgb, g/sum_rgb, b/sum_rgb])
    mean = np.mean(data, axis=0) # mean along columns <=> colors
    std_dev = np.std(data, axis=0)
    for i,color in enumerate(("R","G","B")):
        output[color] = {
                "mean": mean[i],
                "SD": std_dev[i],
                }
    return output


if __name__ == "__main__":
    print(analyse_pseudo_csv(sys.argv[1]))
