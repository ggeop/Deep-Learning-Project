from WebApplication.PythonApp.models.keras_first_go import KerasFirstGoModel


def run_models(user_text):
    first_go_model = KerasFirstGoModel(user_text)
    print(first_go_model)



run_models('data')

