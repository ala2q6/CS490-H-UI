# Imports <
from tensorflow import keras
import numpy as np
import pandas as pd
from os import listdir
from cv2 import imread
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.engine.sequential import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers as tf1, optimizers
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# >


# method loads data from input file
def loadData():

    # local <
    path = 'data'
    data, labels = [], []
    files = [f'{path}/{d}/{i}' for d in listdir(path) for i in listdir(f'{path}/{d}')]

    # >

    # get labels <
    # get data <
    data = list(map(lambda image: imread(image, 1), files))
    labels = list(map((lambda path: 1 if ('galaxy' in path) else 0), files))

    # >

    return data, labels

# >

# method displays a single entry in dataset as image <
def showImg(data, labels, itype):

    plt.imshow(data[itype])
    plt.axis(True)

# >


# Define general purpose graphing function for model history <
def graph(history, gtype):
    plt.plot(history[gtype], label='Train')
    plt.plot(history[f"val_{gtype}"], label='Validation')
    plt.title(gtype)
    plt.ylabel(f"Decimal {gtype}")
    plt.xlabel('Epoch')
    plt.legend()
    # plt.ylim()

# >


if __name__ == "__main__":

    data, labels = loadData()

    # Split dataset into train and test set <
    # Split test set into test and validation set <
    xTrain, xTest, yTrain, yTest = train_test_split(data, labels, test_size=0.2, random_state=42, shuffle=True)
    xTest, xValid, yTest, yValid = train_test_split(xTest, yTest, test_size=0.5, random_state=42, shuffle=True)

    # >

    # Caste input data to np.ndarray <
    xTrain = (np.array(xTrain).astype('float'))
    xTest = (np.array(xTest).astype('float'))
    xValid = (np.array(xValid).astype('float'))
    # Scale input data by 255 <
    # xTrain = (np.array(xTrain).astype('float') / 255.0)
    # xTest = (np.array(xTest).astype('float') / 255.0)
    # xValid = (np.array(xValid).astype('float') / 255.0)

    # >

    # Convert data to one-hot representation in np.ndarray
    yTrain, yTest, yValid = to_categorical(yTrain), to_categorical(yTest), to_categorical(yValid)

    # >



    inputShape = xTrain.shape[1:]
    print(inputShape)
    # Define model layers <
    model = Sequential()
    # Input Layer <
    model.add(tf1.InputLayer(input_shape=inputShape))

    # Scale values for image pixels <
    model.add(tf1.Rescaling(scale=1./255))

    # Flatten input <
    model.add(tf1.Flatten())

    # Functional Layers <
    model.add(tf1.Dense(540, activation='relu'))
    model.add(tf1.Dense(1080, activation='relu'))
    model.add(tf1.BatchNormalization())
    model.add(tf1.Dense(640, activation='relu'))
    # model.add(tf1.Dropout(0.2))
    model.add(tf1.BatchNormalization())
    model.add(tf1.Dense(640, activation='relu'))
    # model.add(tf1.Dropout(0.2))
    model.add(tf1.BatchNormalization())
    model.add(tf1.Dense(340, activation='relu'))

    # Output Layer <
    model.add(tf1.Dense(2, activation='softmax'))

    # >

    # Model Compilation <
    model.compile(

        loss = 'categorical_crossentropy',
        metrics = [tf.keras.metrics.Accuracy(), tf.keras.metrics.AUC()],
        optimizer = optimizers.Adam(learning_rate=0.01)

    )

    # >

    # Fit model to train data <
    history = model.fit(
        xTrain,
        yTrain,
        batch_size = 64,
        epochs = 20,
        verbose = 1,
        validation_data = (xValid, yValid)
    )

    # >

    # Evaluate model execution on test set <
    scores = model.evaluate(xTest, yTest, verbose=1)
    print(f"Test Loss: {scores[0]}")
    print(f"Test Accuracy: {scores[1]}")
    print(f"Test AUC: {scores[2]}")

    # >

    # Display image from dataset <
    showImg(xTest, yTest, 1)
    # >

    # plot accuracy metric <
    graph(history.history, 'accuracy')

    # >

    # plot loss function <
    graph(history.history, 'loss')

    # >

    # plot area under curve metric <
    graph(history.history, list(history.history.keys())[2])

    # >


# Alternative Model Architectures <

# 15%
# model.add(tf1.Flatten(input_shape=(64,64,3)))
# model.add(tf1.Dense(540, activation='relu'))
# model.add(tf1.Dense(1080, activation='relu'))
# model.add(tf1.BatchNormalization())
# model.add(tf1.Dense(640, activation='relu'))
# model.add(tf1.BatchNormalization())
# model.add(tf1.Dense(640, activation='relu'))
# model.add(tf1.BatchNormalization())
# model.add(tf1.Dense(340, activation='relu'))

# 21%
# model.add(tf1.Flatten(input_shape=(64,64,3)))
# model.add(tf1.Dense(540, activation='relu'))
# model.add(tf1.Dense(1080, activation='relu'))
# model.add(tf1.BatchNormalization())
# model.add(tf1.Dense(640, activation='relu'))
# model.add(tf1.BatchNormalization())
# model.add(tf1.Dense(640, activation='relu'))
# model.add(tf1.BatchNormalization())
# model.add(tf1.Dense(340, activation='relu'))

# >
