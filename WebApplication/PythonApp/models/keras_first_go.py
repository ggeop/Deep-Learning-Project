from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras import metrics
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import one_hot

from dataset_handler import DatasetSpliter
from model_utils import conf_keras_first_go

class KerasFirstGoModel(object):
    def __init__(self):
        spliter=DatasetSpliter(conf_keras_first_go.dataset_path,conf_keras_first_go.vocab_size,conf_keras_first_go.max_length)
        split_data=spliter.data_encode()

        self.x_train=split_data[0]
        self.y_train = split_data[1]
        self.x_test = split_data[2]
        self.y_test = split_data[3]
        self.test_labels=spliter.test_labels

        self.create_model()

    def create_model(self):
        self.model = Sequential()
        self.model.add(Dense(conf_keras_first_go.dense, input_shape=(conf_keras_first_go.vocab_size,)))
        self.model.add(Activation(conf_keras_first_go.activation_function))
        self.model.add(Dropout(conf_keras_first_go.dropout))
        self.model.add(Dense(conf_keras_first_go.dense))
        self.model.add(Activation(conf_keras_first_go.activation_function))
        self.model.add(Dropout(conf_keras_first_go.dropout))
        self.model.add(Dense(conf_keras_first_go.labels))
        self.model.add(Activation(conf_keras_first_go.last_activation_function))

        #Compile the model
        self.compile_model()

    def compile_model(self):
        self.model.compile(loss = conf_keras_first_go.loss,
                           optimizer = conf_keras_first_go.optimizer,
                           metrics = [metrics.categorical_accuracy, 'accuracy'])
        # summarize the model
        # print(self.model.summary())

    def create_history(self):
        self.model.fit(self.x_train, self.y_train,
                            batch_size=conf_keras_first_go.batch_size,
                            epochs=conf_keras_first_go.nb_epoch,
                            verbose=conf_keras_first_go.verbose,
                            validation_split=conf_keras_first_go.validation_split)

        score = self.model.evaluate(self.x_test, self.y_test,
                               batch_size=batch_size, verbose=1)

        # print('\nTest categorical_crossentropy:', score[0])
        # print('Categorical accuracy:', score[1])
        # print('Accuracy:', score[2])


    def prediction(self,user_text):

        # Encode the text
        encoded_docs = [one_hot(user_text, conf_keras_first_go.vocab_size)]
        # pad documents to a max length
        padded_text = pad_sequences(encoded_docs, maxlen=conf_keras_first_go.max_length, padding='post')
        # Prediction based on model
        prediction = self.model.predict(padded_text)
        # Decode the prediction
        encoder = LabelBinarizer()
        encoder.fit(self.test_labels)
        result = encoder.inverse_transform(prediction)

        return result[0]
