from flask import Flask, request, render_template , jsonify
from flask_cors import cross_origin
import pandas as pd
import pickle
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

app = Flask(__name__, static_url_path='/static')
with open('latestfile_t.pkl', 'rb') as file:
    model = pickle.load(file)



@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('home.html')



@app.route("/about", methods=['GET'])
@cross_origin()
def about():
    return render_template('aboutus.html')



@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Fetch form data
        date_dep = request.form.get("departure-date")
        date_arr = request.form.get("arrival-date")
        stops = request.form.get("stops")
        airline = request.form.get("airlines")
        from_location = request.form.get("from-location")
        to_location = request.form.get("to-location")

        # Validate inputs
        if not (date_dep and date_arr and stops and airline and from_location and to_location):
            return render_template('home.html', prediction_text="Please fill out all fields.")

        # Check if from and to locations are the same
        if from_location == to_location:
            return render_template('home.html', prediction_text="The departure and destination locations cannot be the same.")

        try:
            # Process dates and times
            Day_of_Journey = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
            Month_of_Journey = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
            Year_of_Journey = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").year)
            Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
            Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
            Arr_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
            Arr_minute = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
            duration_hours = abs(Arr_hour - Dep_hour)
            duration_minute = abs(Arr_minute - Dep_min)
            Total_Stops = int(stops)

            # Prepare dictionaries for categorical variables
            airline_dict = { ... }  # Define dictionary here
            airline_dict[airline] = 1
            source_dict = { ... }   # Define dictionary here
            source_dict[from_location] = 1
            dest_dict = { ... }     # Define dictionary here
            dest_dict[to_location] = 1

            # Predict fare using the model
            prediction = model.predict([[ 
                Total_Stops, Day_of_Journey, Month_of_Journey, Dep_hour, Dep_min, Year_of_Journey,
                Arr_hour, Arr_minute, duration_hours, duration_minute,
                airline_dict['Air India'], 
                airline_dict['GoAir'],
                airline_dict['IndiGo'],
                airline_dict['Multiple carriers'],
                airline_dict['Multiple carriers Premium economy'],
                airline_dict['SpiceJet'], 
                airline_dict['Trujet'],
                airline_dict['Vistara'], 
                airline_dict['Vistara Premium economy'],
                source_dict['Chennai'], 
                source_dict['Delhi'],
                source_dict['Kolkata'], 
                source_dict['Mumbai'],
                dest_dict['Cochin'], 
                dest_dict['New_Delhi'],
                dest_dict['Hyderabad'], 
                dest_dict['Kolkata'],
            ]])
            output = round(prediction[0], 2)
            return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))
        
        except ValueError:
            # Handle the case where conversion fails
            return render_template('home.html', prediction_text="Please enter valid values for all fields.")

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)
