# End_To_End_Flightfare_Prediction

### Current Version: 0.0.1

### Parent Company- IdontKnow

### Deployment Platform: Google Cloud Platform (GCP)

### Project Overview

The **End_To_End_Flightfare_Prediction** project is an advanced machine learning application designed to predict flight fares with high accuracy. This project leverages cutting-edge data science techniques and a robust deployment infrastructure to deliver predictions that can assist users in planning their travel expenses effectively.

### Technologies Used

- **Programming Language**: Python
- **Data Analysis**: NumPy, Pandas, Matplotlib, Seaborn
- **Exploratory Data Analysis (EDA)**: Extensive EDA to understand the data distribution and relationships.
- **Machine Learning**: Scikit-learn with Supervised Learning Algorithms
- **Model Evaluation**: Scikit-learn metrics
- **Backend**: Flask
- **Deployment**: GCP (Google Cloud Platform)
- **Website Development**: HTML, CSS, JavaScript

### Project Workflow

1. **Data Collection**: Gathered historical flight fare data from multiple sources.
2. **Data Cleaning and Preprocessing**: Handled missing values, outliers, and data inconsistencies. Converted categorical data to numerical formats using techniques like one-hot encoding.
3. **Exploratory Data Analysis (EDA)**: Analyzed various features such as date, time, stops, and airline to identify patterns and relationships in the data.
4. **Model Building**: Employed various supervised learning algorithms to build predictive models. Performed hyperparameter tuning to optimize model performance.
5. **Model Evaluation**: Evaluated the models using metrics such as RMSE (Root Mean Squared Error) and R² to ensure accuracy and reliability.
6. **Deployment**: The best-performing model was deployed on Google Cloud Platform using Flask as the backend framework. The web application is hosted on GCP.

### Website

Access the live website here: [End_To_End_Flightfare_Prediction](https://idkflight.wl.r.appspot.com)

### Features

- **Cities Supported**: Kolkata, Mumbai, Delhi, Cochin, Bangalore
- **Accurate Results**: Provides predictions with an error margin of $2 or ₹200
- **User Input Fields**:
  - Date of Arrival
  - Date of Departure
  - Number of Stops
  - Departure City
  - Destination City
  - Airline

### Upcoming Version: 0.1.0

Expected release by the end of the month with the following enhancements:

- **New Data**: Incorporation of the latest flight data.
- **New Cities**: Support for additional cities.
- **Updated Model**: Enhanced model card with improved accuracy, targeting 99% precision.
- **Fine-tuned Biases**: Reduction in prediction biases.
- **Enhanced Website**: Refined UI/UX with additional features.
- **User Management**: Integration of session management, user login, and logout functionality.

### Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/End_To_End_Flightfare_Prediction.git
    ```
2. Navigate to the project directory:
    ```bash
    cd End_To_End_Flightfare_Prediction
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    flask run
    ```
5. Access the application locally:
    ```bash
    http://localhost:5000
    ```

### Requirements

Below is the list of dependencies required to run the project:

```plaintext
blinker==1.8.2
click==8.1.7
contourpy==1.1.1
cycler==0.12.1
Flask==3.0.3
Flask-Cors==4.0.1
fonttools==4.53.0
gunicorn==22.0.0
itsdangerous==2.2.0
Jinja2==3.1.4
joblib==1.4.2
kiwisolver==1.4.5
MarkupSafe==2.1.5
matplotlib==3.7.5
numpy==1.24.4
packaging==24.1
pandas==2.0.3
pillow==10.4.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
pytz==2024.1
scikit-learn==1.3.2
scipy==1.10.1
seaborn==0.13.2
six==1.16.0
threadpoolctl==3.5.0
tzdata==2024.1
Werkzeug==3.0.3
