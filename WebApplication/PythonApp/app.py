import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from models.keras_first_go import KerasFirstGoModel
from clear_bash import clear_bash

app = Flask(__name__)
cleaner=clear_bash()

def train_model():
    global first_go_model

    print("Train the model")
    first_go_model = KerasFirstGoModel()

@app.route("/")
def index():

    return render_template('index.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form.getlist('Job')
      train_model()
      processed_text = first_go_model.prediction(result[0])
      result = {'Job': processed_text}
      return render_template("result.html",result = result)

def clear_bash():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    clear_bash()
    print("---------------------------------")
    print("JOB PREDICTION APPLICATION")
    print("---------------------------------")
    print("\n\n")
    print("--- SET MODE ---")
    print("\n")
    print("Do you want to start the application or test the model? ")
    print("\n")
    print("NOTE: Press 'app' for application of 'model' for model...")
    mode = input()

    if mode=='app':

        clear_bash()

        print("---------------------------------")
        print("JOB PREDICTION APPLICATION")
        print("---------------------------------")
        print(("*Flask starting server..."
                   "please wait until server has fully started"))
        app.run()

    elif mode=='model':

        clear_bash()

        print("---------------------------------")
        print("PLAY WITH KERAS MODEL")
        print("---------------------------------")

        print("Wait until I'm ready..")
        train_model()
        print("\n\n")
        print("OK the model is ready!!")
        skills_description = input("Give me your skill description please: ")
        prediction = first_go_model.prediction(skills_description)
        clear_bash()
        print("This job is my suggetion: ", prediction)
        print("Thanks for all!!")
        clear_bash()

    else:
        print("You are stupid!! BYEEE")
