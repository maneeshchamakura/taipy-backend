from taipy.gui import Gui, notify
import pandas as pd
import yfinance as yf
from taipy.config import Config
import taipy as tp 
import datetime as dt
from taipy import Core
from show_hospitals_map import html_page
from flask import Flask, request, session, jsonify, redirect, render_template
from flask_restful import Api, Resource
import requests

Config.load("config_model_train.toml")
scenario_cfg = Config.scenarios['stock']
tickers = yf.Tickers("msft aapl goog")

root_md = "<|navbar|>"

property_chart = {
    "type": "lines",
    "x": "Date",
    "y[1]": "Open",
    "y[2]": "Close",
    "y[3]": "High",
    "y[4]": "Low",
    "color[1]": "green",
    "color[2]": "grey",
    "color[3]": "red",
    "color[4]": "yellow",
}
df = pd.DataFrame([], columns=["Date", "High", "Low", "Open", "Close"])
df_pred = pd.DataFrame([], columns = ['Date','Close_Prediction'])

stock = ""
stock_text = "No Stock to Show"
chart_text = "No Chart to Show"
stocks = []


page = """
# Stock Portfolio

### Choose the stock to show
<|toggle|theme|>

<|layout|columns=1 1|
<|
<|{stock_text}|>

<|{stock}|selector|lov=MSFT;AAPL;GOOG;Reset|dropdown|>

<|Press for Stock|button|on_action=on_button_action|>
<|Get the future predictions|button|on_action=get_predictions|>
|>

<|{stock}
<|{chart_text}|>
<|{df}|chart|properties={property_chart}|>
|>

|>
"""

pages = {
    "/" : root_md,
    "home" : page,
    "claim": "empty page"
}

def on_button_action(state):
    if state.stock == "Reset":
        state.stock_text = "No Stock to Show"
        state.chart_text = "No Chart to Show"
        state.df = pd.DataFrame([], columns=["Date", "High", "Low", "Open", "Close"])
        state.df_pred = pd.DataFrame([], columns = ['Date','Close_Prediction'])
        state.pred_text = "No Prediction to Show"
    else:
        state.stock_text = f"The stock is {state.stock}"
        state.chart_text = f"Monthly history of stock {state.stock}"
        state.df = tickers.tickers[state.stock].history().reset_index()
        state.df.to_csv(f"{stock}.csv", index=False)



def get_predictions(state):
    
    scenario_stock = tp.create_scenario(scenario_cfg)
    scenario_stock.initial_dataset.path = f"{stock}".csv
    notify(state, 'success', 'camehere')
    scenario_stock.write(state.df)
    tp.submit(scenario_stock)
    state.df_pred = scenario_stock.predictions.read()
    state.df_pred.to_csv("pred.csv", index=False)

tp.Core().run()
# Gui(pages=pages).run(use_reloader=True)


app = Flask(__name__)
# app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management
api = Api(app)

class SignupResource(Resource):
    def get(self):
        return redirect("/signup.html")
    
    def post(self):
        SIGNUP_API_URL = "https://health-insurance-rest-apis.onrender.com/api/signup"
        signup_data = {
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email']
        }
        headers = {
            'Content-Type': 'application/json'
        }
        print(signup_data)
        response = requests.post(SIGNUP_API_URL, headers=headers, json=signup_data)
        print("response", response)
        if response.status_code == 200:
            return redirect("/login.html")
        else:
            return 'Signup Failed'

# Login Resource
class LoginResource(Resource):
    def get(self):
        """
        Return a simple login page HTML
        """
        return redirect("/login.html")
    def post(self):
        email = request.form['email']
        password = request.form['password']
        auth_data = {
            'username': email,
            'password': password
        }
        AUTH_API_URL = "https://health-insurance-rest-apis.onrender.com/api/login"
        response = requests.post(AUTH_API_URL, json=auth_data)
        if response.status_code == 200:
            auth_data = response.json()
            access_token = auth_data.get('access_token')
            refresh_token = auth_data.get('refresh_token')

            # Store tokens in the session
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token

            return redirect("/home")
        else:
            return 'Login failed', 401

# Protected Resource
class ProtectedResource(Resource):
    def get(self):
        # Check if the JWT token is present in the session
        if 'jwt_token' in session:
            jwt_token = session['jwt_token']

            # You can add logic here to verify the JWT token if needed
            # For simplicity, we assume the token is valid

            return {'message': 'Access granted for protected route', 'jwt_token': jwt_token}, 200
        else:
            return {'message': 'Access denied'}, 401

print("registered the apis")
# Add resources to the API
api.add_resource(LoginResource, '/login')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(SignupResource, '/signup')

@app.before_request
def check_access_token():
    # print ('access_token' in session, "checkIt")
    if request.endpoint != 'login' and 'access_token' not in session:
    #     # Redirect to the login page if not on the login route and no access_token is in the session
    #     print(request.endpoint, "endpoint")
        return redirect("/login")

gui = Gui(pages=pages, flask=app).run()
