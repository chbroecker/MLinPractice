#!/bin/bash

# create directory if not yet existing
mkdir -p data/feature_extraction/

# run feature extraction on training set (may need to fit extractors)
echo "  training set"
python -m src.feature_extraction.extract_features data/preprocessing/split/training.csv data/feature_extraction/training.pickle -e data/feature_extraction/pipeline.pickle --verbose --char_length --media_type --day_period --weekday --keywords 10 --common_words 10

# run feature extraction on validation set and test set (with pre-fit extractors)
echo "  validation set"
python -m src.feature_extraction.extract_features data/preprocessing/split/validation.csv data/feature_extraction/validation.pickle -i data/feature_extraction/pipeline.pickle --char_length --media_type --day_period --weekday --keywords 10 --common_words 10
echo "  test set"
python -m src.feature_extraction.extract_features data/preprocessing/split/test.csv data/feature_extraction/test.pickle -i data/feature_extraction/pipeline.pickle --char_length --media_type --weekday --day_period --keywords 10 --common_words 10
