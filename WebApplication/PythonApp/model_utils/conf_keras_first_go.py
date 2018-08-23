
########################################################
########### MODEL CONFIGURATION FILE ###################
########################################################

#Dataset path
dataset_path ='./data/25_cleaned_job_descriptions.csv'

#Parameters
vocab_size=500
max_length=500
batch_size = 500
nb_epoch = 30

#Model Parameters
dense=512
dropout=0.1
labels=25
activation_function='relu'
last_activation_function='softmax'

#Complile Parameters
optimizer = 'adam' # or 'sgd'
loss = 'categorical_crossentropy'

#Model fit
validation_split=0.1
verbose=1
