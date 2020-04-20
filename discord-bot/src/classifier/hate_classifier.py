from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

import nltk
from nltk.stem.porter import *

# Embedding
max_features = 36300
maxlen = 33
embedding_size = 128

model = load_model('hate_speech_model.h5')

model.summary()

class hate_classifier:

    def preprocess(self,message):
        punctuation = "!\"#$%&()*+,'-./:;<=>?@[\]^_`{|}~"
        table = str.maketrans("","",punctuation)

        stemmer = PorterStemmer()
        processed_msg = message.lower().translate(table).split()
        processed_msg = [stemmer.stem(t) for t in processed_msg]
        processed_msg = " ".join(processed_msg)
        print(processed_msg)
        return processed_msg

    def encode(self,message):
        encoded = one_hot(message, max_features)
        encoded = pad_sequences([encoded], dtype='int32', padding='post', value=0, maxlen=maxlen)
        return encoded

    def classify(self, encoding):
        result = model.predict(encoding)
        print(result)
        result = result[0][0]
        return result

    def predict(self, message):
        return self.classify(self.encode(self.preprocess(message)))

