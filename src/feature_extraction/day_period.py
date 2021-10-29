#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple feature that represents the day period as integer

Created on Fri Oct 29 12:57:14 2021

@author: ldankert
"""

import numpy as np
from src.feature_extraction.feature_extractor import FeatureExtractor


# class for extracting the character-based length as a feature
class DayPeriod(FeatureExtractor):

    # constructor
    def __init__(self, input_column):
        super().__init__([input_column], input_column)

    # don't need to fit, so don't overwrite _set_variables()

    # compute the word length based on the inputs
    def _get_values(self, inputs):
        result = []
        for period in np.array(inputs[0]):
            if period == "Night":
                period_number = 0
            elif period == "Morning":
                period_number = 1
            elif period == "Afternoon":
                period_number = 2
            elif period == "Evening":
                period_number = 3
            else:
                raise Exception("The day period is not defined, it was: {}".format(period))
            result.append(period_number)
        result = np.array(result)
        result = result.reshape(-1, 1)
        return result
