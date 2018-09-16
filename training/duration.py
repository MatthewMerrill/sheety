import keras
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

batch_size = 128
num_classes = 3
epochs = 12

img_rows, img_cols = 36, 104

train = pd.read_csv('training/durations.csv').values
test = pd.read_csv('training/durations.csv').values

trainX = train[:,1:].reshape(train.shape[0], 1, 28, 28) astype('float32');
X_train = trainX / 2

