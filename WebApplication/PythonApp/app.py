from flask import Flask, flash, redirect, render_template, request, session, abort
from models.keras_first_go import KerasFirstGoModel
app = Flask(__name__)

print("Create the model")
first_go_model = KerasFirstGoModel()

@app.route("/")
def index():

    return render_template('index.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form.getlist('Job')
      print(result[0])
      processed_text = first_go_model.prediction(result[0])
      print(processed_text)
      result = {'Job': processed_text}
      return render_template("result.html",result = result)

if __name__ == "__main__":
    print("Start the server")
    app.run()