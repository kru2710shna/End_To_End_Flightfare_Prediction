from flask import Flask, request, render_template
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



@app.route("/predict", methods=["GET","POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        
        
        # Fetching form data
        date_dep = request.form["departure-date"]
        Day_of_Journey = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Month_of_Journey = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        Year_of_Journey = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").year)
        
        #Depature
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
        
        #ARRIVAL
        date_arr = request.form["arrival-date"]
        Arr_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arr_minute = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
        
        #Duration
        duration_hours = abs(Arr_hour - Dep_hour)
        duration_minute = abs(Arr_minute - Dep_min)
        
        #Stops
        stops = request.form["stops"]
        Total_Stops = int(stops)


        airline = request.form['airlines']
        # Prepare dictionaries for categorical variables
        airline_dict = {
            'Air India': 0, 'GoAir': 0, 'IndiGo': 0,
            'Multiple carriers': 0, 'Multiple carriers Premium economy': 0, 
            'SpiceJet': 0,  'Trujet': 0, 'Vistara': 0, 
            'Vistara Premium economy': 0
        }
        airline_dict[airline] = 1


        from_location = request.form["from-location"]
        source_dict = {
            'Chennai': 0, 'Delhi': 0, 'Kolkata': 0, 'Mumbai': 0
        }
        source_dict[from_location] = 1
        
        
        to_location = request.form["to-location"]
        dest_dict = {
            'Cochin': 0, 'New_Delhi': 0,
            'Hyderabad': 0, 'Kolkata': 0
        }
        dest_dict[to_location] = 1
        
         # Validate inputs
        if not (date_dep and date_arr and stops and airline and from_location and to_location):
            return render_template('home.html', prediction_text="Please fill out all fields.")


        # Predict fare using the model
        prediction = model.predict([[
            Total_Stops, Day_of_Journey, Month_of_Journey, Dep_hour, Dep_min,Year_of_Journey,
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
        
        return render_template('home.html',  prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)
