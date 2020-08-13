# mongoDB to DataFrame

import pandas as pd
import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.0.154:27017/')  # mongo 연결
mydb = client.mydb

modelDB = mydb.processed # get Collection

model_df = pd.DataFrame(list(modelDB.find()))

## modeling 1 - 독립변수 빈도에 따른 인코딩 없이 진행

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.initializers import Constant
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score 


# x, y 데이터 넣기
x = model_df['total']
y = model_df['score']

# x 데이터 토크나이징
MAX_LEN=35 # 한 행의 최대 단어 수인 것 같음
tokenizer=Tokenizer()
tokenizer.fit_on_texts(x)
sequences=tokenizer.texts_to_sequences(x)
total_pad = pad_sequences(sequences,maxlen=MAX_LEN,truncating='post',padding='post')
word_index=tokenizer.word_index
print('Number of unique words:',len(word_index))

# y 데이터 범주화 (인코딩)
for i in range(len(y)):
    if y[i] == 'A':
        y[i] = 1
    else:
        if y[i] == 'B':
            y[i] = 2
        else:
            if y[i] == 'C':
                y[i] = 3
            else:
                y[i] = 4

from tensorflow.keras.utils import to_categorical

y_cate = to_categorical(y)
y_cate

# 모델링
num_words = len(word_index)+1

x_train_all, x_test, y_train_all, y_test = train_test_split(total_pad, y_cate, test_size=0.3, random_state=1)
x_train, x_val, y_train, y_val = train_test_split(x_train_all, y_train_all, test_size=0.2, random_state=1)

model=Sequential()

embedding_layer=Embedding(num_words, 32, input_length=MAX_LEN, trainable=False)  #embeddings_initializer=Constant(embedding_matrix) 제외

model.add(embedding_layer)
model.add(SpatialDropout1D(0.2))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2,return_sequences=True))
model.add(tf.keras.layers.LSTM(64,return_sequences=True))
model.add(tf.keras.layers.LSTM(32))
model.add(tf.keras.layers.Dense(8, activation='relu'))
model.add(Dense(5, activation='softmax'))

early_stopp = tf.keras.callbacks.EarlyStopping(monitor = 'loss', patience = 3, restore_best_weights = True)
optimizer = Adam(learning_rate = 1e-4)

model.compile(loss = 'categorical_crossentropy', optimizer = optimizer, metrics = ['accuracy'])
history = model.fit(x_train, y_train, batch_size = 128, epochs = 500, validation_data = (x_val, y_val), callbacks = [early_stopp],verbose = 1)