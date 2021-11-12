#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keyword class for feature extractor

Created: 11.11.21, 22:47

Author: LDankert
"""


import numpy as np
import nltk
from collections import Counter
from sklearn.preprocessing import MultiLabelBinarizer
from src.feature_extraction.feature_extractor import FeatureExtractor


# class for extracting the character-based length as a feature
class Keyword(FeatureExtractor):

    # constructor
    def __init__(self, input_column, number_of_keywords):
        super().__init__([input_column], "keywords")
        self.number_of_keywords = number_of_keywords

    # set the variables depending on the number of keywords
    def _set_variables(self, inputs):
        all_tweets = []
        for tweet in inputs[0]:
            all_tweets.extend(tweet)

        freq = nltk.FreqDist(all_tweets)
        self.keywords = freq.most_common(self.number_of_keywords)
        print(f"    The {self.number_of_keywords} most common keywords:")
        for keyword in self.keywords:
            print(f"    {keyword[0]}: {keyword[1]}")

    # returns columns, one for each most common words one
    def _get_values(self, inputs):
        result = []
        keywords = [keyword for keyword, _ in self.keywords]
        for tweet in inputs[0]:
            keywords_in_tweet = []
            keywords_in_tweet += [keyword for keyword in keywords if keyword in tweet]
            result.append(keywords_in_tweet)

        enc = MultiLabelBinarizer()
        result = enc.fit_transform(result)
        return result
