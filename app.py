from flask import Flask, request, render_template
from flask_cors import cross_origin
import pandas as pd
import pickle

app = Flask(__name__, static_url_path='/static')
with open('finalfile.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('home.html')

@app.route("/about", methods=['GET'])
@cross_origin()
def about():
    return render_template('aboutus.html')

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        try:
            # Fetching form data
            date_dep = request.form["departure-date"]
            date_arr = request.form["arrival-date"]
            stops = request.form["stops"]
            airline = request.form['airlines']
            from_location = request.form["from-location"]
            to_location = request.form["to-location"]

            # Validate inputs
            if not (date_dep and date_arr and stops and airline and from_location and to_location):
                return render_template('home.html', prediction_text="Please fill out all fields.")

            # Convert fields to appropriate types
            Day_of_journey = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day
            Month_of_journey = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month
            Year_of_journey = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").year
            Dep_hour = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour
            Dep_min = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute
            Arr_hour = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour
            Arr_minute = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute
            dur_hour = abs(Arr_hour - Dep_hour)
            dur_min = abs(Arr_minute - Dep_min)
            Total_Stops = int(stops)

            # Prepare dictionaries for categorical variables
            airline_dict = {
                'Air India': 0, 'GoAir': 0, 'IndiGo': 0,
                'Multiple carriers': 0, 'Multiple carriers Premium economy': 0, 
                'SpiceJet': 0,  'Trujet': 0, 'Vistara': 0, 
                'Vistara Premium economy': 0
            }
            airline_dict[airline] = 1

            source_dict = {
                'Source_Chennai': 0, 'Source_Delhi': 0, 'Source_Kolkata': 0, 'Source_Mumbai': 0, 'Source_Banglore': 0
            }
            source_dict[from_location] = 1

            dest_dict = {
                'Destination_Cochin': 0, 'Destination_Delhi': 0, 'Destination_New Delhi': 0,
                'Destination_Hyderabad': 0, 'Destination_Kolkata': 0, 'Destination_Banglore': 0
            }
            dest_dict[to_location] = 1

            # Predict fare using the model
            prediction = model.predict([[
                Total_Stops, Day_of_journey, Month_of_journey, Dep_hour, Dep_min,Year_of_journey,
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

        except ValueError as e:
            return render_template('home.html', prediction_text="Error predicting fare. Please check your inputs and try again.")

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
