import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.text import Tokenizer

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

        # parameters
        vocab_size = 1000

        # define Tokenizer with Vocab Size
        tokenizer = Tokenizer(num_words=vocab_size)
        tokenizer.fit_on_texts(self.train_descs)
        x_train = tokenizer.texts_to_matrix(self.train_descs, mode='tfidf')
        x_test = tokenizer.texts_to_matrix(self.test_descs, mode='tfidf')

        encoder = LabelBinarizer()
        encoder.fit(self.train_labels)
        y_train = encoder.transform(self.train_labels)
        y_test = encoder.transform(self.test_labels)

        return x_train, y_train, x_test, y_test

