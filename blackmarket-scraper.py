
import schedule
import time
import secrets
import json
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import logging
from pymongo import MongoClient
from datetime import datetime, timedelta
import os



# Connect to the MongoDB database
client = MongoClient('mongodb+srv://ayoseun:Jared15$@cashflakes.dgkmv.mongodb.net/Auth?retryWrites=true&w=majority')
db = client['bmr']  # Replace with your actual database name
collection = db['users']

app = Flask(__name__)

# Set up logging
if not app.debug:
    logging.basicConfig(filename='app.log', level=logging.ERROR)

# Set up environment variables
API_KEY = os.getenv('API_KEY')

# Make a request to https://www.ngnrates.com/black-market
@app.route('/', methods=['GET'])
def index():
    """Return a welcome message."""
    return "Welcome to the Black Market Rate API. For markets data, visit this route /market"

@app.route('/market', methods=['GET'])
def scrape():
  
    key = request.args.get('key')
    if not key:
        return jsonify({"error": "API key is missing."}), 400

    # Check if the API key exists in the database
    user = collection.find_one({"userKey": key})
    if not user:
        return jsonify({"error": "Invalid API key."}), 401

     # Check if the elapsedTime is less than today
    elapsed_time = user.get('elapsedTime')
    if elapsed_time < datetime.now():
        return jsonify({"error": "Elapsed time has expired."}), 403
    # Rest of your code

    try:
        page = requests.get('https://www.ngnrates.com/black-market')
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract the table from the page
        table = soup.find('table', {'class': 'table table-condensed table-striped'})
        if table:
            # Extract the headings
            headings = [th.text.strip() for th in table.find("thead").find_all("th")]
            # Extract the rows
            rows = table.find("tbody").find_all("tr")
            # Initialize an array to store the objects
            data = []
            # Iterate over the rows
            for row in rows:
                # Extract the cells
                cells = row.find_all("td")
                # Extract the currency, date, and rate information
                currency = cells[0].text.strip()
                rate = cells[1].text.strip().replace('\u20a6', '')
                date = cells[2].text.strip()
                # Store the information as an object in the array
                data.append({"Currency": currency, "Rate": str(rate), "Date": date})
            # Return the data as JSON
            return jsonify(data)
        else:
            # Log an error if the table is not found
            error_msg = "Table not found."
            logging.error(error_msg)
            return jsonify({"error": error_msg}), 404
    except Exception as e:
        # Log the error and return a 500 status code
        error_msg = f"Error: {str(e)}"
        logging.error(error_msg)
        return jsonify({"error": error_msg}), 500



@app.route('/user', methods=['POST'])
def generate():
    """Add user data to the database."""
    data = request.get_json()
    elapsed_time = data.get('elapsedTime')
    address = data.get('elapsedTime')
    if not address or data is None:
        return jsonify({"error": "Empty payload. User wallet address and elapsed time are required."}), 400

    # Check if elapsed_time is not an integer
    if not isinstance(elapsed_time, int):
        return jsonify({"error": "Invalid value for elapsed time. Expected an integer."}), 400

    # Generate a random hex user key
    user_key = secrets.token_hex(16)

    # Convert elapsed_time to a valid datetime object
    try:
        if elapsed_time == 30:
            elapsed_time = datetime.now() + timedelta(days=30)
        elif elapsed_time == 60:
            elapsed_time = datetime.now() + timedelta(days=60)
        elif elapsed_time == 90:
            elapsed_time = datetime.now() + timedelta(days=90)
        elif elapsed_time == 365:
            elapsed_time = datetime.now() + timedelta(days=365)
        else:
            raise ValueError("Invalid value for elapsed time.")
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid value for elapsed time. Expected a valid integer."}), 400

    # Create the user data object
    user_data = {
        "userKey": user_key,
        "address":address,
        "elapsedTime": elapsed_time
    }

    # Insert the user data into the database
    result = collection.insert_one(user_data)

    return jsonify({"response": "User data added successfully.", "inserted_id": str(result.inserted_id),"key": str(user_key)}), 201
# ...




def scrape_and_log():
    """Scrape the data and log any errors."""
    try:
        data = scrape()
        # Write the data to a JSON file
        with open('data.json', 'w') as f:
            json.dump(data, f)
        print("Data scraped successfully.")
        logging.error(data)
    except Exception as e:
        # Log the error and raise it to halt the program
        error_msg = f"Error: {str(e)}"
        logging.error(error_msg)
        raise e

# Schedule the scraping to run every 10 minutes
schedule.every(5).minutes.do(scrape_and_log)

if __name__ == '__main__':
    while True:
        # Run the scheduled tasks
        schedule.run_pending()
        # Wait 1 second before checking for scheduled tasks again
        time.sleep(1)
        # Start the Flask app
        app.run(debug=False)




