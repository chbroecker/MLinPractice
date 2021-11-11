#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stemming the inputed words

Created on Thu Nov 09 19:50:23 2021

@author: ldankert
"""

from src.preprocessing.preprocessor import Preprocessor
import nltk

class Lowercaser(Preprocessor):
    """Stemmes every word in the input string"""
    
    def __init__(self, input_column, output_column):
        """Initialize the Stemmer with the given input and output column."""
        super().__init__([input_column], output_column)
    
    # don't need to implement _set_variables(), since no variables to set
    
    def _get_values(self, inputs):
        """Stemmes the tweet."""
        
        lowercased = []
        for tweet in inputs[0]:
            lowercased.append([word.lower() for word in tweet])
        return lowercase