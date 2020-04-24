import tensorflow as tf
from sklearn.model_selection import train_test_split
import re
import numpy as np
import pandas as pd

MAX_WORDS = 16
from tensorflow.keras.models import load_model


# model = tf.keras.models.model_from_json("")

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


    # def preprocess(self,message):
        # punctuation = "!\"#$%&()*+,'-./:;<=>?@[\]^_`{|}~"
        # table = str.maketrans("","",punctuation)
        #
        # stemmer = PorterStemmer()
        # print(message)
        # processed_msg = message.lower().translate(table).split()
        # processed_msg = [stemmer.stem(t) for t in processed_msg]
        # processed_msg = " ".join(processed_msg)
        # print(processed_msg)
        # return processed_msg

    # def encode(self,message):
    #
    #     encoded = one_hot(message, max_features)
    #     print(encoded)
    #     encoded = pad_sequences([encoded], dtype='int32', padding='post', value=0, maxlen=maxlen)
    #     print(encoded)
    #     return encoded
    #
    # def classify(self, encoding):
    #     result = model.predict(encoding)
    #     print(result)
    #     result = result[0][0]
    #     print(result)
    #     result = result >= classifier_threshold
    #     print(result)
    #     return result

    # def predict(self, message):
    #     return self.classify(self.encode(self.preprocess(message)))

    def encode_tf(self, message):
        message = [remove_mentions(message)]
        x_seq = self.tk.texts_to_sequences(message)
        return tf.keras.preprocessing.sequence.pad_sequences(x_seq, maxlen=MAX_WORDS, padding="post", truncating="post")


classifier = hate_classifier()
with open("./network_tf_lstm.json", "r") as f:
    model = tf.keras.models.model_from_json(f.read())
    model.load_weights("./network_tf_lstm.h5")

encoded = classifier.encode_tf("test")

prediction = model.predict(classifier.encode_tf("zxcvbnm"))
if len(prediction) == len("I hate bananas"):
    print("Character encoding.")
print(sum(prediction))
# print(type(model.predict(classifier.encode_tf('I hate bananas'))))
print("")