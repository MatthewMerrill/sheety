from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convo2D, MaxPooling2D
from keras import backend as K

batch_size = 128
num_classes = 3
epochs = 12

img_rows, img_cols = 28, 28



