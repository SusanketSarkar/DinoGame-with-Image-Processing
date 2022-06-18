import cv2
import pandas as pd
import time, sys
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from keras.utils import to_categorical
from PIL import Image

global df

df = pd.DataFrame(columns=['Image', 'Action'])


def capture_do_nothing():
    global df
    camera = cv2.VideoCapture(0)
    exit = False
    while not exit:
        cv2.namedWindow('Capture your gesture for the dino to run!!!') 
        cv2.resizeWindow('Capture your gesture for the dino to run!!!', 300, 350)
        return_value, image = camera.read()
        cv2.imshow('Capture your gesture for the dino to run!!!', image)
        count = 0
        if cv2.waitKey(1) & 0xFF == ord('s'):
            while count != 1500:
                im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(im)
                im = im.resize((100, 100))
                im = np.array(im)
                append_to_df(im, 0)
                count += 1
                return_value, image = camera.read()
                cv2.imshow('Capture your gesture for the dino to run!!!', image)
                cv2.waitKey(1)
                num = int((count/1500)*50)
                sys.stdout.write("=="+"="*(num)+'>'+"-"*(50-num)+str(count)+'/1500')
                sys.stdout.flush()
                time.sleep(0.5)
            exit = True
    camera.release()
    cv2.destroyAllWindows()


def capture_jump():
    global df
    camera = cv2.VideoCapture(0)
    exit = False
    while not exit:
        cv2.namedWindow('Capture your gesture for the dino to jump!!!')
        cv2.resizeWindow('Capture your gesture for the dino to jump!!!', 300, 350)
        return_value, image = camera.read()
        cv2.imshow('Capture your gesture for the dino to jump!!!', image)
        count = 0
        if cv2.waitKey(1) & 0xFF == ord('s'):
            while count != 1500:
                im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(im)
                im = im.resize((100, 100))
                im = np.array(im)
                append_to_df(im, 1)
                count += 1
                return_value, image = camera.read()
                cv2.imshow('Capture your gesture for the dino to jump!!!', image)
                cv2.waitKey(1)
                num = int((count/1500)*50)
                sys.stdout.write("=="+"="*(num)+'>'+"-"*(50-num)+str(count)+'/1500')
                sys.stdout.flush()
                time.sleep(0.5)
            exit = True
    camera.release()
    cv2.destroyAllWindows()


def append_to_df(image, action):
    global df
    df = df.append({'Image': image, 'Action': int(action)}, ignore_index=True)


def prepare_dataset():
    global df
    df = df.sample(frac=1).reset_index(drop=True)
    X = df.iloc[:, 0]
    Y = df.iloc[:, 1]
    x = []
    for i in range(X.shape[0]):
        x.append(X[i])
    x = np.asarray(x)
    x = (x.astype(float) - 128) / 128
    x = np.reshape(x, (X.shape[0], 100, 100, 3))
    y = to_categorical(Y)
    return x, y


def load_model():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), strides=(1, 1), activation='relu', input_shape=(100, 100, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.8))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def train(model, X, y):
    model.fit(X, y, batch_size=64, epochs=1, shuffle=True)


def save_model(model):
    model.save_weights('weightsrecorded.h5')


if __name__ == '__main__':
    capture_do_nothing()
    time.sleep(1)
    capture_jump()
    time.sleep(1)
    X, y = prepare_dataset()
    model = load_model()
    train(model, X, y)
    save_model(model)