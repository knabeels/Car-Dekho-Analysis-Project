from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type=request.form['Fuel_Type']
        if (Fuel_Type == 'CNG'):
            Fuel_Type = 0
        elif(Fuel_Type == 'Diesel'):
                Fuel_Type = 1
        else:
            Fuel_Type = 2
        
        Year = 2023-Year
        
        Seller_Type = request.form['Seller_Type']
        if(Seller_Type == 'Individual'):
            Seller_Type = 1
        else:
            Seller_Type = 0
        
        Transmission = request.form['Transmission']
        if(Transmission == 'Manual'):
            Transmission = 1
        else:
            Transmission = 0
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type,Seller_Type,Transmission]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

