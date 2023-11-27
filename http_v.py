from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Set up logging
if not app.debug:
    logging.basicConfig(filename='app.log', level=logging.ERROR)

# Set up environment variables
API_KEY = os.getenv('API_KEY')

# Set up environment variables
MARKET_RATE_URL = os.getenv('MARKET_RATE_URL')
# Make a request
@app.route('/', methods=['GET'])
def index():
    """Return a welcome message."""
    return "Welcome to the Black Market Scraping API. For data, visit /market"

@app.route('/market', methods=['GET'])
def scrape():
    """Scrape the black market exchange rates and return the data as JSON."""
    try:
        page = requests.get(MARKET_RATE_URL)
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

if __name__ == '__main__':
    app.run(debug=True, port=8080)
