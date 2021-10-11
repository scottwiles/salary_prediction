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

@app.route('/submit-predictions', methods = ['POST'])
def submit_predictions():
    print("Request from the front-end:")
    req = request.get_json()
    if isinstance(req, dict):
        req = [req]

    req_df = pd.DataFrame(req)

    predicted_salary = model.predict(req_df)
    
    print(req_df, end = '\n\n')
    print(f"Predicted salary: {predicted_salary}", end = '\n\n')
    return {'message': predicted_salary.tolist()}

if __name__ == "__main__":
    debug_value = False
    if len(sys.argv) > 1 and sys.argv[1] == '--dev':
        print("\nRunning with dev mode enabled\n")
        debug_value = True

    app.run(debug=debug_value)
