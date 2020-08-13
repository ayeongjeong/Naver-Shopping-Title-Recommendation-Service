import tensorflow as tf
import re
import keras
from keras.models import Model, Sequential
from keras.layers import Dense, LSTM, Embedding
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.optimizers import RMSprop
from keras.preprocessing.sequence import pad_sequences
import pickle


# sub_data = {'category':'50000145', 'product':'미숫가루','title':'국산 곡물 100% 미숫가루'}
sub_data = {'category':'50000145', 'product':'닭가슴살','title':'햇살닭 닭가슴살 10팩 스테이크 한입'}

def clean_str(text):
    pattern = '[-=,#/\?:^$.@\"※~&ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl=' ', string=text)   # repl 띄어쓰기!
    return text

clean_title = clean_str(sub_data['title'])

model_input = sub_data['category']+" "+sub_data['product']+" "+clean_title

token = pickle.load(open("./webservice/tokenizer.pkl", "rb"))
# tokenizer=Tokenizer()

def modeling_NAUM(data):
    data = data.replace("   "," ")
    data = data.replace("  "," ")
    MAX_LEN=150
    # tokenizer.fit_on_texts(data)
    sequences = token.texts_to_sequences([data])
    total_pad = pad_sequences(sequences,maxlen=MAX_LEN,truncating='post',padding='post')
    # print(total_pad)
    # word_index=tokenizer.word_index
    first_model = tf.keras.models.load_model('webservice/modeling_NAUM.h5')
    # print(total_pad[0])
    testdata = total_pad
    result = first_model.predict(testdata)
    return result

p=modeling_NAUM(model_input)
print(p)