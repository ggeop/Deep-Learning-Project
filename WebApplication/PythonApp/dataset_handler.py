import pandas as pd
from keras.preprocessing.text import one_hot
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.sequence import pad_sequences


class DatasetSpliter(object):

    def __init__(self):
        self.data = pd.read_csv('./data/25_cleaned_job_descriptions.csv', header = 0, names = ['Query', 'Description'])
        self.split_data()
        self.vocab_size=500
        self.max_length=500
        self.split_data()

    def split_data(self):
        # Split data to train and test (80 - 20)
        train, test = train_test_split(self.data, test_size=0.2)

        self.train_descs = train['Description']
        self.train_labels = train['Query']

        self.test_descs = test['Description']
        self.test_labels = test['Query']

    def data_encode(self):

        ###Training Data
        # Encode the jobs descriptions
        encoded_docs = [one_hot(d, self.vocab_size) for d in self.train_descs]
        # pad documents to a max length
        x_train = pad_sequences(encoded_docs, maxlen=self.max_length, padding='post')
        #Binarize the job titles
        encoder = LabelBinarizer()
        encoder.fit(self.train_labels)
        y_train = encoder.transform(self.train_labels)

        ###Test Data
        # Encode the jobs descriptions
        encoded_docs = [one_hot(d, self.vocab_size) for d in self.test_descs]
        # pad documents to a max length
        x_test = pad_sequences(encoded_docs, maxlen=self.max_length, padding='post')
        #Binarize the job titles
        encoder = LabelBinarizer()
        encoder.fit(self.test_labels)
        y_test = encoder.transform(self.test_labels)

        return x_train, y_train, x_test, y_test

