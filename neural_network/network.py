import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation, Embedding, GlobalAveragePooling1D
from keras.layers.core import Dense, Flatten
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from numpy import array
import pandas as pd
import io


data_frame = pd.read_csv('labeled_data.csv')  #io.StringIO(uploaded['labeled_data.csv'].decode('utf-8')))

tweets = data_frame['tweet']
print(tweets)
labels = data_frame['hate_speech']
print(labels)


processed_tweets = []

punctuation = "!\"#$%&()*+,'-./:;<=>?@[\]^_`{|}~"
table = str.maketrans("","",punctuation)

for tweet in tweets:
    processed_tweets.append(tweet.lower().translate(table))
    #processed_tweets.append(text_to_word_sequence(tweet, filters="!\"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n", lower=True, split=" "))
#print(processed_tweets[0])

encoded_tweets = [one_hot(tweet, 50000) for tweet in processed_tweets]

#print(encoded_tweets[0])

padded_tweets = pad_sequences(encoded_tweets, dtype='int32', padding='post', value=0)


binary_labels = []

for label in labels:
    if label > 0:
        binary_labels.append(1)
    else:
        binary_labels.append(0)

train_tweets = padded_tweets[:20000]
test_tweets = padded_tweets[20000:]

train_labels = binary_labels[:20000]
test_labels = binary_labels[20000:]

print(binary_labels)

#unique, counts = np.unique(labels.values, return_counts=True)
#dict(zip(unique, counts))

# I used this to print an output file of just the tweets labeled "1"
# Don't need it anymore, will remove it later
#index = 0
#with open("output.txt", "w") as ofile:
#    for tweet in tweets:
#        if labels[index] == 1:
#            ofile.write(tweet)
#            ofile.write("\n")
#        index += 1

model = Sequential([Embedding(input_dim=50000, output_dim=512, input_length = 33),
                    #GlobalAveragePooling1D(), This gave less accuracy than Flatten
                    Flatten(),
                    Dense(512, activation='relu'),
                    Dense(256, activation='relu'),
                    Dense(128, activation='relu'),
                    Dense(64, activation='relu'),
                    Dense(32, activation='relu'),
                    Dense(16, activation='relu'),
                    Dense(1, activation='sigmoid')
                    ])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.summary()


fit_model = model.fit(x=train_tweets, y=train_labels, batch_size=32, epochs=10, verbose=1, validation_split=0.2, shuffle=True)

score = model.evaluate(test_tweets, test_labels, batch_size=32)
print(str(round(score[1]*100,2))+"%")