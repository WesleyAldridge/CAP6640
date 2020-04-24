import tensorflow as tf
from sklearn.model_selection import train_test_split
import re
import numpy as np
import pandas as pd

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
EPOCHS = 10
BATCH_SIZE = 256
MAX_WORDS = 64
df = pd.read_csv('../data/t-davidson data/labeled_data.csv')
df = df.reindex(np.random.permutation(df.index))
df = df[["tweet", "hate_speech"]]

# we only want 0 or 1 for hate speech
df["hate_speech"] = pd.Series(np.where(df["hate_speech"].values > 0, 1, 0), df.index)

df["tweet"] = df["tweet"].apply(remove_mentions)
X_train, X_test, Y_train, Y_test = train_test_split(
    df["tweet"].values,
    df["hate_speech"].values,
    test_size=0.2,
    random_state=67)
tk = tf.keras.preprocessing.text.Tokenizer(num_words=VOCAB_SIZE, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                           lower=True, split=" ")
tk.fit_on_texts(X_train)
X_train_seq = tk.texts_to_sequences(X_train)
X_test_seq = tk.texts_to_sequences(X_test)
X_train_seq_pad = tf.keras.preprocessing.sequence.pad_sequences(X_train_seq, maxlen=MAX_WORDS)
X_test_seq_pad = tf.keras.preprocessing.sequence.pad_sequences(X_test_seq, maxlen=MAX_WORDS)

model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(input_dim=50000, output_dim=512, input_length=64),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
    ])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_model = model.fit(X_train_seq_pad, Y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=1, shuffle=True)
# fit_model = model.fit(train_data, batch_size=32, epochs=10)

# score = model.evaluate(X_test, Y_test, batch_size=BATCH_SIZE)
