import pickle
import numpy as np
import pandas as pd
from keras.models import load_model
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    price = request.json.get('price')
    open_price = request.json.get('open')
    high = request.json.get('high')
    low = request.json.get('low')
    volume = request.json.get('volume')
    change = request.json.get('change')
    model = request.json.get('model')
    print('./models/' + model + '.keras')

    loaded_model = load_model('./models/' + model + '.keras')
    with open('./models/' + model + '.pkl', 'rb') as f:
        sc = pickle.load(f)

    data = {
        'Price': price,
        'Open': open_price,
        'High': high,
        'Low': low,
        'Vol.': volume,
        'Change %': change,
    }

    testing_data = pd.Series(data).values.reshape(1, -1) if model not in ['DNN', 'LSTM', 'GRUs', 'MERGE'] else pd.Series(data).values.reshape(1, -1).repeat(61, axis=0)
    input = sc.transform(testing_data)
    predicted_price = np.array(loaded_model.predict(np.array([input]))).reshape(-1)
    
    return jsonify({'price': str(predicted_price[0])}), 200

if __name__ == "__main__":
    app.run(debug=True)