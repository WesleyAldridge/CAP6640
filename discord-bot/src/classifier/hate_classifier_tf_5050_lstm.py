import re
import tensorflow as tf
import pandas as pd
import numpy as np

MAX_WORDS = 16

# Model reconstruction from JSON file
with open('network_tf_5050_lstm.json', 'r') as f:
    model = tf.keras.models.model_from_json(f.read())

# Load weights into the new model
model.load_weights('network_tf_5050_lstm.h5')

model.summary()

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
        df = pd.read_csv("../data/labeled_data_5050.csv")
        self.tk = tf.keras.preprocessing.text.Tokenizer(num_words=50000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                                        lower=True, split=" ")
        self.tk.fit_on_texts(df["tweet"])

    def encode(self, message):
        message = [remove_mentions(message)]
        x_seq = self.tk.texts_to_sequences(message)
        return tf.keras.preprocessing.sequence.pad_sequences(x_seq, maxlen=MAX_WORDS)

    def classify(self, encoding):
        result = model.predict(encoding)
        print(result)
        result = result[0][0]
        return result

    def predict(self, message):
        return self.classify(self.encode(message))
