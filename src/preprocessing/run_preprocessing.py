#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runs the specified collection of preprocessing steps

Created on Tue Sep 28 16:43:18 2021

@author: lbechberger
"""

import argparse, csv, pickle
import pandas as pd
from sklearn.pipeline import make_pipeline
from src.preprocessing.punctuation_remover import PunctuationRemover
from src.preprocessing.tokenizer import Tokenizer
from src.preprocessing.stopword_remover import StopwordRemover
from src.preprocessing.lowercaser import Lowercaser
from src.preprocessing.stemmer import Stemmer
from src.util import COLUMN_TWEET, COLUMN_TWEET_CLEANED


# setting up CLI
parser = argparse.ArgumentParser(description = "Various preprocessing steps")
parser.add_argument("input_file", help = "path to the input csv file")
parser.add_argument("output_file", help = "path to the output csv file")
parser.add_argument("-c", "--clean", action="store_true", help= "Use all nltk preprocessing features")
parser.add_argument("-e", "--export_file", help = "create a pipeline and export to the given location", default = None)
args = parser.parse_args()

# load data
df = pd.read_csv(args.input_file, quoting = csv.QUOTE_NONNUMERIC, lineterminator = "\n")

# collect all preprocessors
preprocessors = []
if args.clean:
    preprocessors.append(PunctuationRemover(COLUMN_TWEET, COLUMN_TWEET_CLEANED))
    preprocessors.append(Lowercaser(COLUMN_TWEET_CLEANED, COLUMN_TWEET_CLEANED))
    preprocessors.append(Tokenizer(COLUMN_TWEET_CLEANED, COLUMN_TWEET_CLEANED))
    preprocessors.append(StopwordRemover(COLUMN_TWEET_CLEANED, COLUMN_TWEET_CLEANED))
    preprocessors.append(Stemmer(COLUMN_TWEET_CLEANED, COLUMN_TWEET_CLEANED))

# call all preprocessing steps
for preprocessor in preprocessors:
    df = preprocessor.fit_transform(df)

# store the results
df.to_csv(args.output_file, index = False, quoting = csv.QUOTE_NONNUMERIC, line_terminator = "\n")

# create a pipeline if necessary and store it as pickle file
if args.export_file is not None:
    pipeline = make_pipeline(*preprocessors)
    with open(args.export_file, 'wb') as f_out:
        pickle.dump(pipeline, f_out)
