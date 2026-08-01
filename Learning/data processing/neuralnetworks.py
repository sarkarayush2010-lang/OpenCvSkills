import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import fashion_mnist
import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten

(traindata, trainlabels), (testdata, testlabels) = fashion_mnist.load_data()
print("Training data shape:", traindata.shape)

traindata = traindata / 255.0
testdata = testdata / 255.0

model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(traindata, trainlabels, epochs=5, batch_size=32)

test_loss, test_acc = model.evaluate(testdata, testlabels)

model.save("fashionmodel.h5")
