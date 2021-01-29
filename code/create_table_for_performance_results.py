"""
File name: create_table_for_performance_results.py
Author: Esra Zihni
Date created: 21.05.2018

This script creates a table of the overall performance results. It reads the 
implementation and path options from the config.yml script. It reads the training and 
test performance results calculated using the specified performance measure(s) for 
the specified number of splits. It calculates the median and IQR of the performance 
scores over the splits and stores them in a pandas.DataFrame. Finally, it saves the 
table of performance scores as a csv file.
"""

import itertools
import os

import numpy as np
import pandas as pd
import yaml
from scipy.stats import iqr
from utils.helper_functions import config_handler


def create_table_for_performance_results():

    ########################################################################################
    ###### ASSIGN CONFIGURATION VARIABLES ##################################################
    ########################################################################################

    # You need to add constructor in order to be able to use the join command in the yaml
    # file
    def join(loader, node):
        seq = loader.construct_sequence(node)
        return "".join(str(i) for i in seq)


    yaml.add_constructor("!join", join)

    # Read the config file
    cfg = yaml.load(open("config.yml", "r"), Loader=yaml.Loader)


    # Assign variables to use
    dataset_name = cfg["dataset name"]
    #models_to_use = cfg["models to use"]
    models_to_use,explainability_measures = config_handler(cfg)
    subsampling_types = cfg["subsampling to use"]
    performance_measures = cfg["final performance measures"]
    scores_folder = cfg["scores folder path"]
    feature_dict = cfg["features"]


    ########################################################################################
    ###### CREATE TABLE OF ALL PERFORMANCE SCORES ##########################################
    ########################################################################################

    # Check if the scores file path already exists.
    if not os.path.isfile(f"{scores_folder}/{dataset_name}_performance_results.csv"):
        values = ["median", "iqr"]
        iterables = [subsampling_types, models_to_use, values]
        multiidx = pd.MultiIndex.from_product(
            iterables, names=["Subsampling Type", "Model", "Value"]
        )
        scoring = [" (training)", " (test)"]
        performance_index = [
            "".join(item)
            for item in itertools.product(
                [pm.replace("_", " ") for pm in performance_measures], scoring
            )
        ]

        df = pd.DataFrame([], columns=performance_index, index=multiidx)

        for perf, subs, mdl in itertools.product(
            performance_measures, subsampling_types, models_to_use
        ):
            model_results = pd.read_csv(
                f"{scores_folder}/{mdl}_{perf}_scores_{subs}_subsampling.csv", index_col=0
            )
            df.loc[(subs, mdl), perf.replace("_", " ") + " (training)"] = (
                "{:.2f}".format(np.median(model_results, axis=0)[0]),
                "{:.2f}".format(iqr(model_results, axis=0)[0]),
            )
            df.loc[(subs, mdl), perf.replace("_", " ") + " (test)"] = (
                "{:.2f}".format(np.median(model_results, axis=0)[1]),
                "{:.2f}".format(iqr(model_results, axis=0)[1]),
            )

        df.to_csv(f"{scores_folder}/{dataset_name}_performance_results.csv")
