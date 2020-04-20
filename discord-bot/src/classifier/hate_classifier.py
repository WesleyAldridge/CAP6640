from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import tensorflow as tf
import pandas as pd

from tensorflow.keras.models import load_model

import nltk
from nltk.stem.porter import *

# Embedding
max_features = 36300
maxlen = 33
embedding_size = 128
classifier_threshold = 0.5

model = load_model('hate_speech_model.h5')

# https://github.com/bertcarremans/TwitterUSAirlineSentiment/blob/master/source/Using%20Word%20Embeddings%20for%20Sentiment%20Analysis.ipynb
def remove_mentions(input_text):
    '''
    Function to remove mentions, preceded by @, in a Pandas Series

    Parameters:
        input_text : text to clean
    Output:
        cleaned Pandas Series
    '''
    return re.sub(r'@\w+', '', input_text)

class hate_classifier:

    def __init__(self):
        df = pd.read_csv("../../../data/t-davidson data/labeled_data.csv")
        self.tk = tf.keras.preprocessing.text.Tokenizer(num_words=50000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                                   lower=True, split=" ")
        self.tk.fit_on_texts(df["tweet"])


    def preprocess(self,message):
        punctuation = "!\"#$%&()*+,'-./:;<=>?@[\]^_`{|}~"
        table = str.maketrans("","",punctuation)

        stemmer = PorterStemmer()
        print(message)
        processed_msg = message.lower().translate(table).split()
        processed_msg = [stemmer.stem(t) for t in processed_msg]
        processed_msg = " ".join(processed_msg)
        print(processed_msg)
        return processed_msg

    def encode(self,message):

        encoded = one_hot(message, max_features)
        print(encoded)
        encoded = pad_sequences([encoded], dtype='int32', padding='post', value=0, maxlen=maxlen)
        print(encoded)
        return encoded

    def classify(self, encoding):
        result = model.predict(encoding)
        print(result)
        result = result[0][0]
        print(result)
        result = result >= classifier_threshold
        print(result)
        return result

    def predict(self, message):
        return self.classify(self.encode(self.preprocess(message)))

    def encode_tf(self, message):
        message = remove_mentions(message)
        x_seq = self.tk.texts_to_sequences(message)
        return tf.keras.preprocessing.sequence.pad_sequences(x_seq, maxlen=64)