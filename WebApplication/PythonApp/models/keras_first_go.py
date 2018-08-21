from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras import metrics
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import one_hot

from dataset_handler import DatasetSpliter


class KerasFirstGoModel(object):

    def __init__(self):
        spliter=DatasetSpliter()
        split_data=spliter.data_encode()

        self.x_train=split_data[0]
        self.y_train = split_data[1]
        self.x_test = split_data[2]
        self.y_test = split_data[3]
        self.test_labels=spliter.test_labels
        self.create_model()

    def create_model(self):
        #parameters
        num_labels = 25
        vocab_size = 1000

        self.model = Sequential()
        self.model.add(Dense(512, input_shape=(vocab_size,)))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(512))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(num_labels))
        self.model.add(Activation('softmax'))

        # compile the model
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

        self.compile_model()
        # summarize the model
        # print(self.model.summary())

    def compile_model(self):
        self.model.compile(loss = 'categorical_crossentropy',
                           optimizer = 'adam', # or 'sgd'
                           metrics = [metrics.categorical_accuracy, 'accuracy'])

    def create_history(self):
        # parameters
        batch_size = 500
        nb_epoch = 30

        # fit the model
        self.model.fit(self.x_train, self.y_train,
                            batch_size=batch_size,
                            epochs=nb_epoch,
                            verbose=1,
                            validation_split=0.1)

        score = self.model.evaluate(self.x_test, self.y_test,
                               batch_size=batch_size, verbose=1)

        print('\nTest categorical_crossentropy:', score[0])
        print('Categorical accuracy:', score[1])
        print('Accuracy:', score[2])


    def prediction(self,user_text):
        # parameters
        max_length = 1000
        vocab_size = 1000

        # Encode the text
        encoded_docs = [one_hot(user_text, vocab_size)]

        # pad documents to a max length
        padded_text = pad_sequences(encoded_docs, maxlen=max_length, padding='post')

        # Prediction based on model
        prediction = self.model.predict(padded_text)

        # Decode the prediction
        encoder = LabelBinarizer()
        encoder.fit(self.test_labels)
        result = encoder.inverse_transform(prediction)

        return result[0]

