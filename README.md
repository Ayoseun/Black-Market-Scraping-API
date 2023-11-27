# Black-Market-Scraping-API
This API is written is python and uses Flask to scrape the internet for blackmarket naira price
# Black Market Scraping API
Welcome to the Black Market Scraping API, a Flask-based web application that scrapes black market exchange rates from a website and returns the data as JSON. This API is designed to be simple and easy to use, making it ideal for developers who need real-time access to black market exchange rates.

### Installation
To install the necessary dependencies for this application, run the following command:

create a virtual environment
```
python3 -m venv [your environment name]
```

##### activate the environment
On Mac (Command Prompt):
```
source myenv/bin/activate
```

On Linux (Command Prompt):
```
myenv\Scripts\activate.bat
```

On Windows (PowerShell):
```
myenv\Scripts\Activate.ps1
```

```
pip install -r requirements.txt
```
Usage
To run the application, execute the following command:

```
gunicorn blackmarket-scraper:app 

```
This will start the Flask development server, which you can access by visiting http://localhost:5000 in your web browser.

To run the application, execute the following command to capture output:

```
gunicorn blackmarket-scraper:app --capture-output

```

Once the server is running, you can use the following API endpoints to retrieve data:
/ - Returns a welcome message
/market - Scrapes black market exchange rates and returns the data as JSON
To automate the scraping function and run it every 10 minutes, you can use a task scheduling library like Celery or APScheduler. Alternatively, you can use a cloud-based service like AWS Lambda or Google Cloud Functions to run the scraping function on a schedule.

### Configuration
This application uses environment variables to store sensitive information like API keys. To set these variables, create a .env file in the root directory of the application and add the following lines:



API_KEY=<your_api_key_here>

Replace <your_api_key_here> with your actual API key. Note that this file should not be committed to version control, as it contains sensitive information.

License
This project is licensed under the MIT License - see the LICENSE file for details.


