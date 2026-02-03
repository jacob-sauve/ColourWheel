#!../../../venv/bin/python3
import sys
import numpy as np


def analyse_pseudo_csv(filepath):
    """analyse us sensor output from file at filepath"""
    data = list()
    output = dict()
    with open(filepath, 'r') as file:
        for line in file:
            data.append(float(line))
    output["mean"] = np.mean(data)
    output["std_dev"] = np.std(data)
    output["mini"],output["maxi"] = min(data), max(data)
    return output


if __name__ == "__main__":
    print(analyse_pseudo_csv(sys.argv[1]))
