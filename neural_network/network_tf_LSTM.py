import tensorflow as tf
from sklearn.model_selection import train_test_split
import re
import numpy as np
import pandas as pd
import pickle

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

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


VOCAB_SIZE = 50000
EPOCHS = 25
BATCH_SIZE = 128
MAX_WORDS = 16
NAME="network_tf_lstm"

df = pd.read_csv('../data/labeled_data_5050.csv')
# df = df.reindex(np.random.permutation(df.index))
df = df[["tweet", "label"]]

# we only want 0 or 1 for hate speech
df["label"] = pd.Series(np.where(df["label"].values > 0, 1, 0), df.index)

df["tweet"] = df["tweet"].apply(remove_mentions)
X_train, X_test, Y_train, Y_test = train_test_split(
    df["tweet"].values,
    df["label"].values,
    test_size=0.2,
    random_state=67)
tk = tf.keras.preprocessing.text.Tokenizer(num_words=VOCAB_SIZE, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                           lower=True, split=" ")
tk.fit_on_texts(X_train)
X_train_seq = tk.texts_to_sequences(X_train)
X_test_seq = tk.texts_to_sequences(X_test)
X_train_seq_pad = tf.keras.preprocessing.sequence.pad_sequences(X_train_seq, maxlen=MAX_WORDS, padding="post", truncating="post")
X_test_seq_pad = tf.keras.preprocessing.sequence.pad_sequences(X_test_seq, maxlen=MAX_WORDS, padding="post", truncating="post")

model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(input_dim=50000, output_dim=512, input_length=MAX_WORDS),
    tf.keras.layers.LSTM(MAX_WORDS, input_shape=(None, 512)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(4, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
    ])

summary = model.summary()
pickle.dump(summary, open("{}_summary.pickle".format(NAME), "wb"))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train_seq_pad, Y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=1, shuffle=True, validation_split=0.2)

evaluation = model.evaluate(X_test_seq_pad, Y_test, batch_size=BATCH_SIZE)
pickle.dump(evaluation, open("{}_evaluation.pickle".format(NAME), "wb"))
json = model.to_json()
with open("./{}.json".format(NAME), "w") as json_file:
    json_file.write(json)
model.save_weights("./{}.h5".format(NAME))
