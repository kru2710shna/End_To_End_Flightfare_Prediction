from flask import Flask, request, render_template
from flask_cors import cross_origin
import pandas as pd
import pickle

app = Flask(__name__, template_folder='Front-End')
model = pickle.load(open("flight_rf.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Date_of_Journey
        date_dep = request.form["departure-date"]
        Journey_day = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day
        Journey_month = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month

        # Departure
        Dep_hour = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour
        Dep_min = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute

        # Arrival
        date_arr = request.form["arrival-date"]
        Arrival_hour = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour
        Arrival_min = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_Stops = int(request.form["stops"])

        # Airline
        airline = request.form['airlines']
        airline_dict = {
            'Airline_Air India': 0, 'Airline_GoAir': 0, 'Airline_IndiGo': 0,
            'Airline_Jet Airways': 0, 'Airline_Multiple carriers': 0,
            'Airline_Multiple carriers Premium economy': 0, 'Airline_SpiceJet': 0,
            'Airline_Trujet': 0, 'Airline_Vistara': 0, 'Airline_Vistara Premium economy': 0
        }
        airline_dict[airline] = 1

        # Source
        Source = request.form["from-location"]
        source_dict = {
            'Source_Chennai': 0, 'Source_Delhi': 0, 'Source_Kolkata': 0, 'Source_Mumbai': 0
        }
        source_dict[Source] = 1

        # Destination
        Destination = request.form["to-location"]
        dest_dict = {
            'Destination_Cochin': 0, 'Destination_Delhi': 0, 'Destination_New Delhi': 0,
            'Destination_Hyderabad': 0, 'Destination_Kolkata': 0
        }
        dest_dict[Destination] = 1

        # Predicting Fare
        prediction = model.predict([[
            Total_Stops, Journey_day, Journey_month, Dep_hour, Dep_min,
            Arrival_hour, Arrival_min, dur_hour, dur_min,
            airline_dict['Airline_Air India'], airline_dict['Airline_GoAir'],
            airline_dict['Airline_IndiGo'], airline_dict['Airline_Jet Airways'],
            airline_dict['Airline_Multiple carriers'],
            airline_dict['Airline_Multiple carriers Premium economy'],
            airline_dict['Airline_SpiceJet'], airline_dict['Airline_Trujet'],
            airline_dict['Airline_Vistara'], airline_dict['Airline_Vistara Premium economy'],
            source_dict['Source_Chennai'], source_dict['Source_Delhi'],
            source_dict['Source_Kolkata'], source_dict['Source_Mumbai'],
            dest_dict['Destination_Cochin'], dest_dict['Destination_Delhi'],
            dest_dict['Destination_Hyderabad'], dest_dict['Destination_Kolkata'],
            dest_dict['Destination_New Delhi']
        ]])

        output = round(prediction[0], 2)

        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
