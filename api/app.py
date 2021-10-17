import sys
from flask import Flask, send_from_directory, request
import pandas as pd
import pickle

with open('../models/salary_prediction_xgboost_v1.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__, static_folder='../front-end/build', static_url_path='')

@app.route('/')
@app.route('/index')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')


@app.route('/single-prediction', methods = ['POST'])
def submit_predictions():
    
    req = request.get_json()
    # for single items the 'req' object will be a dictionary, wrapping it in a list is 
    # convenient for pd.DataFrame()
    if isinstance(req, dict):
        req = [req]

    req_df = pd.DataFrame(req)
    predicted_salary = model.predict(req_df)
    
    return {'message': predicted_salary.tolist()}


@app.route('/multiple-prediction', methods = ['POST'])
def multi_predict():
    # Get json data from request
    req = request.get_json()
    # Make a DataFrame and separate the id's for each row of data
    req_df = pd.DataFrame(req)
    output_ids = req_df.id

    req_df.drop(columns='id', inplace=True)
    # Get predictions, convert to list because np.array is not JSON serializable
    preds = model.predict(req_df).tolist()

    output = {id:pred for id, pred in zip(output_ids, preds)}

    return {'message': output}


if __name__ == "__main__":
    debug_value = False
    if len(sys.argv) > 1 and sys.argv[1] == '--dev':
        print("\nRunning with dev mode enabled\n")
        debug_value = True

    app.run(debug=debug_value)
