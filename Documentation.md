# Documentation Example

Some introductory sentence(s). Data set and task are relatively fixed, so 
probably you don't have much to say about them (unless you modifed them).
If you haven't changed the application much, there's also not much to say about
that.
The following structure thus only covers preprocessing, feature extraction,
dimensionality reduction, classification, and evaluation.

## Major pipeline changes
Due to major errors in executing the pipeline on my Linux Machine, I had to
change the folder name of `code` into `src`. Therefore, I had to change some
bash commands accordingly.

## 1 Evaluation
TODO: baselines

For the evaluation metrics we have implemented all the ones we learned about during the course. We are also using all evaluation metrics in our classification because due to `mlflow` we aren't getting overwelmed with all the different numbers. They all get logged and then later we can  analyze our classifiers depending an different evaluation metrics and we don't have to rerun the pipeline if we want to use a differnt one. 
The evaluation metrics we implemented are the following:  
* `accuracy`
* `cohen's kappa`
* `precision`
* `f1 score`
* `recall`
  
We will skip describing how each of them work because this was covered in the course but we just wanted to mention that we mostly looked at `Cohen's kappa` for our evaluation due to its robustness. 


## 2 Preprocessing

The major part of our preprocessing was to break the original tweet down into usable single strings. Therefore we had to first remove the punctuation in the tweet and then turn all letters into lowercase letters. Following that we split the long sentence strings into single word strings (tokenization). With these tokens we can then remove stopwords like 'the', 'a', etc. pretty easily and then finally stemm all words (i.e. gaming --> game, gamer --> game). We are doing the stemming because we then want to analyze all the tweets to find the most common keywords that are being used.

### Modules:
* `punctuation_remover.py`: searches along every single tweet for a punctuation. When it founds one it replaces it with `""`. After that it returns the punctuation free tweets as a list.
* `lowercaser.py`: takes a list of input tweets and changes all uppercase letters in the tweet to lowercase letters. After that it returns the lowercased tweets as a list.
* `tokenizer.py`: takes a list of input tweets and splits them up into the words as single strings. It uses `nltk.word_tokenizer` for this and returns a list of lists of strings. One list that contains a list with the words of the tweet as its items. (We changed the predefined functionality a little bit)
* `stopword_remover.py`: We want to remove the stopwords that were already mentioned above to make later language processing easier. The stopword remover receives the tokenized tweet. It iterates over all these words and just returns the ones, which are not in `nltk.corpus.stopwords('english)`
* `stemmer.py`: Because we later want to determine general themes in the tweets we want to stem the words inside the tweets. What this does is explained above. We use the porter stemmer (`nltk.stem.PorterStemmer`) to stem all words in the cleaned up 
tweets and return them.

|Example tweet:                 |`['This is the coolest example tweeter!']`
|-------------------------------|:---------------------------------
|1. Remove punctuation returns: |['This is the coolest example tweeter']`
|2. Change to lowercase:        |['this is the coolest example tweeter']
|3. Split up into tokenz:       |['this', 'is', 'the', 'coolest', 'example', 'tweeter']
|4. Remove stop words:          |['coolest', 'example', 'tweeter']
|5. Stem all remaining words:   |['cool', 'example', 'tweet']

### Test:
We created unittests for all our newly created preprocessing modules. The folder `src/test/preprocessing/` contains:ee
* `lowercaser_test.py`
* `tokenizer_test.py`
* `stopword_remover_test.py`
* `stemmer_test.py`
For all functions we have example inputs and compare them to the expected output. We also check, if ethe parente
preprocessor class works as expected and test the naming and the other functions.

### Motivation:
We implemented all preprocessing modules separately, because we can then combine them and extract different features from the different preprocessed columns.
For our features we just needed the complete cleaned data. Punctuation would mess up the feature,
because the punctuation characters would reach a high count, without containing any information. The same goes for the stop words. To stem the tweets properly, they needed to all be in lowercase and tokenized. With this now cleaned up tweet we can extract the most common words and the words with 
the highest virality.

## 3 Feature Extraction
TODO: plots of the distributions
TODO: Can we already guess which features may be more useful than others?

For the feature extraction we used the predefined `feature_extractor` and 
`feature_collector`. The feature_extractor class initializes the according
feature and transforms it later onto the data set, the feature_collector 
collectes all features after they got created and fit them onto the data.
To train a classifier later, the feature extractor needs to return one coloumn
for every single feature, containing the information.

The different feature names are:
* `character_length`
* `media_type` 
* `day_period` 
* `weekday` 
* `most_common_words` 
* `keyword` 

### Character Length:
This feature computes the length of the tweets. Therefore it takes the tweets 
and just computes the string length for every tweet and returns a list with 
one column containing the length as an integer.

### Media Type:
The media type extractor needs two columns from the original data frame to
compute the features. The column `photo` from the original dataset contains 
either the hyperlink of the posted picture, or `"[]"` whenever no photo is
attached. The `video` column contains two different values `1` and `0`.
Intuitively we thought `1` stands for "contains a video" and `0` for "no video". 
However, with a detailed look at the dataset, we recognized, that it is `1` if a photo
is attached too and only `0` when neither a photo or a video is attached. To
correct this data confusion, we define that the tweet contains a video 
whenever `video` is `1` AND `photo` is `"[]"`. The `_get_values` method checks
every tweet for a media file and returns according to that one column for each
photo, video and none:

| 'photos' | 'video' | result|
|----------|:--------|------:|
['Some photo url']  | [1] | [1,0,0]|
['[]']  | [1] | [0,1,0]|
['[]']  | [0] | [0,0,1]|

### Day Period:
The day period extractor depends on mainly one column, namely the column `time`. The 
time is represented as a string with the format 'hh:mm:ss'. Therefore we could
use the inbuild python method `split` with ":" as seperator to get the needed 
hour part. We didn't use any other information. With the extracted hour we 
could then check, in which interval and at which day period the 
post was created.
* 0  - 6  -> night
* 6  - 12 -> morning 
* 12 - 18 -> afternoon
* 18 - 24 -> evening

We used the `sklearn.preprocessing.OneHotEncoder` to transform this categorical
feature into single binary columns:

| ID     |'time'    |categori   |OneHotVector|
|-------:|:---------|:----------|:-----------|
|295806  | 18:29:04 |  2        |[0,0,1,0]   |
|295807  | 07:46:31 |  1        |[0,1,0,0]   |
|295808  | 03:24:09 |  0        |[1,0,0,0]   |
|295809  | 00:29:44 |  0        |[1,0,0,0]   |
|295810  | 19:45:15 |  3        |[0,0,0,1]   |

### Weekday:
The weekday extractor works basically like the day period extractor. The original
column is now 'date', and the format looks as follows: 'YYYY-MM-DD'. To categorize
this data, we used the pandas method `to_datetime` and `dt.dayofweek`. This 
results in one column of integers between 0 and 6 according to the weekday. 
The `OneHotEncoder` again transforms this categorical data into binary 
feature vectors.

| ID     |'date'    |categori   |OneHotVector   |
|-------:|:---------|:----------|:--------------|
|295806  |2018-10-20|  5        |[0,0,0,0,0,1,0]|
|295807  |2018-10-18|  3        |[0,0,0,1,0,0,0]|
|295808  |2019-09-18|  2        |[0,0,1,0,0,0,0]|
|295809  |2018-02-18|  0        |[1,0,0,0,0,0,0]|
|295810  |2018-02-17|  6        |[0,0,0,0,0,0,1]|

### Most common words:
The most common words feature not depends on meta data like the privous one, but on 
the preprocessed and cleaned tweets. In the `_set_variabels` method it combines all 
tweets into one, long list, containing all upcomming words of all posts. Within the 
`nltk.FreqDist` class we then determine the most common words and print them. How 
many most common words we extract can be adjusted with the CLI. We chose to take the 
10 most common words. To extract the final features, we use the most common words
to determine if one or multiple common words appear in the tweets. If so it creates a 
list for every tweet containing all existing common words. The `sklearn.preprocessing.MultiLabelBinarizer` turns this list of lists into a binary vector, one for each common word.

Example:
MostCommonWord: ["example1", "example2, "example3"]

|Tweet                           | Result |
|--------------------------------|:-------|
|["example2","example3",example9]|[0,1,1] |
|["example5","example3",example0]|[0,0,0] |
|["example2","example3",example1]|[1,1,1] |
|["example2","example2",example0]|[1,0,0] |

### Keyword:
The Keyword feature works the exact same as the `most common words` feature except that it only takes the tweets into account that have gone viral. 


## 4 Dimensionality Reduction

The idea of dimensionality reduction is to analyze the feature space that is made up by all the available features and to try to reduce its dimensionality. 
In the ideal case unnecessary or redundant features can be removed and by doing that the whole complexity of the system and the required computation time to train it go down. Dimensionality reduction can only be used to its full potential when the number of features goes up. In our case this wasn't the case until the very end so we didn't focus a lot on it. 

During the course `SelectKBest` was implemented and we then also added `Principal component analysis (PCA)` afterwards. 
Running either `PCA` or `SelectKBest` didn't seem to have any effect on our performance and we even saw that we even have a very slightly better performance without running any form of dimensionality reduction. This is why we decided to not put a big focus on the dimensionality reduction for now. This does not mean that dimensionality reduction is not a big part of an ML pipeline but that in order to effectively use it we would need more features first.


## 5 Classification

Apart from 



### Design Decisions

Which classifier(s) did you use? Which hyperparameter(s) (with their respective
candidate values) did you look at? What were your reasons for this?

### Results

The big finale begins: What are the evaluation results you obtained with your
classifiers in the different setups? Do you overfit or underfit? For the best
selected setup: How well does it generalize to the test set?

### Interpretation

Which hyperparameter settings are how important for the results?
How good are we? Can this be used in practice or are we still too bad?
Anything else we may have learned?




## Summary

Our main hypothesis about why our classification is not performing so well is that we do not have many "natural language features". Because both of our team members do not have a lot of NLP experience we decided to focus more on the meta data than on the actual text content of the tweet. Sitting here now we think that the content of the tweet is probably a lot more important than e.g. the time of day when it was posted. A bigger focus on actual NLP features like `n-grams`, `TF-IDF` or `word embeddings` would have most likely resulted in significantly improved classification performance.

