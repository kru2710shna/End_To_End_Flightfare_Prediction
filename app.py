from flask import Flask, request, render_template
from flask_cors import cross_origin
import pandas as pd
import joblib

app = Flask(__name__, template_folder='templates')
model = joblib.load('model_packet')

@app.route("/")
@cross_origin()
def home():
    return render_template('home.html')

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        date_dep = request.form["departure-date"]
        
        # Date of Journey
        Day_of_journey = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day
        Month_of_journey = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month

        # Departure
        Dep_hour = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour
        Dep_min = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute

        # Arrival
        date_arr = request.form["arrival-date"]
        Arr_hour = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour
        Arr_minute = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute

        # Duration
        dur_hour = abs(Arr_hour - Dep_hour)
        dur_min = abs(Arr_minute - Dep_min)

        # Total Stops
        Total_Stops = int(request.form["stops"])

        # Airline
        airline = request.form['airlines']
        
        airline_dict = {
            'Air India': 0, 'GoAir': 0, 'IndiGo': 0,
            'Multiple carriers': 0, 'Multiple carriers Premium economy': 0, 
            'SpiceJet': 0,  'Trujet': 0, 'Vistara': 0, 
            'Vistara Premium economy': 0
        }
        airline_dict[airline] = 1

        # Source
        Source = request.form["from-location"]
        source_dict = {
            'Source_Chennai': 0, 'Source_Delhi': 0, 'Source_Kolkata': 0, 'Source_Mumbai': 0, 'Source_Banglore':0
        }
        source_dict[Source] = 1

        # Destination
        Destination = request.form["to-location"]
        dest_dict = {
            'Destination_Cochin': 0, 'Destination_Delhi': 0, 'Destination_New Delhi': 0,
            'Destination_Hyderabad': 0, 'Destination_Kolkata': 0, 'Destination_Banglore':0
        }
        
        dest_dict[Destination] = 1

        # Predicting Fare
        prediction = model.predict([[
            Total_Stops, Day_of_journey, Month_of_journey, Dep_hour, Dep_min,
            Arr_hour, Arr_minute, dur_hour, dur_min,
            airline_dict['Air India'], 
            airline_dict['GoAir'],
            airline_dict['IndiGo'],
            airline_dict['Multiple carriers'],
            airline_dict['Multiple carriers Premium economy'],
            airline_dict['SpiceJet'], 
            airline_dict['Trujet'],
            airline_dict['Vistara'], 
            airline_dict['Vistara Premium economy'],
            source_dict['Source_Chennai'], 
            source_dict['Source_Delhi'],
            source_dict['Source_Kolkata'], 
            source_dict['Source_Mumbai'],
            dest_dict['Destination_Cochin'], 
            dest_dict['Destination_Delhi'],
            dest_dict['Destination_Hyderabad'], 
            dest_dict['Destination_Kolkata'],
            dest_dict['Destination_New Delhi']
        ]])

        output = round(prediction[0], 2)

        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
