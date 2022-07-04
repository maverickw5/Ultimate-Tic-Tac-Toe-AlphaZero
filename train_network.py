from dual_network import DN_INPUT_SHAPE
from tensorflow.keras.callbacks import LearningRateScheduler, LambdaCallback, EarlyStopping
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np
import pickle
import matplotlib.pyplot as plt

TRAIN_EPOCH = 100

def load_data(): #load history file
    history_path = sorted(Path('./data').glob('*.history'))[-1]
    with history_path.open(mode='rb') as f:
        return pickle.load(f)

def train_network():
    history = load_data()
    xs, y_policies, y_values = zip(*history)
    a, b, c = DN_INPUT_SHAPE
    xs = np.array(xs)
    xs = xs.reshape(len(xs), c, a, b).transpose(0, 2, 3, 1)
    y_policies = np.array(y_policies)
    y_values = np.array(y_values)

    model = load_model('./model/best.h5') #loads best model
    model.compile(loss=['categorical_crossentropy', 'mse'], optimizer='adam')
    
    def step_decay(epoch): #adjust learning rate after 50th and 80th iteration
        x = 0.001
        if epoch >= 50: x = 0.0005
        if epoch >= 80: x = 0.00025
        return x

    lr_decay = LearningRateScheduler(step_decay)
    print_callback = LambdaCallback(on_epoch_begin=lambda epoch, logs:
        print('\rTrain {}/{}'.format(epoch + 1, TRAIN_EPOCH), end=''))
    hist = model.fit(xs, [y_policies, y_values], batch_size=32, epochs=TRAIN_EPOCH, verbose=0, callbacks=[lr_decay, print_callback])
    print('')
    model.save('./model/latest.h5') #saves to latest model
    K.clear_session()
    del model
    #plots the loss
    plt.plot(hist.history['loss'])
    plt.plot(hist.history['p_loss'])
    plt.plot(hist.history['v_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['pieces', 'policies', 'values'], loc='upper left')
    plt.show()

if __name__ == '__main__':
    train_network()