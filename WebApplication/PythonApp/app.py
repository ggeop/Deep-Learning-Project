from flask import Flask, flash, redirect, render_template, request, session, abort
from models.keras_first_go import KerasFirstGoModel
app = Flask(__name__)

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

if __name__ == "__main__":

    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))

    app.run()