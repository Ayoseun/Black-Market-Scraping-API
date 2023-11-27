from flask import Flask
from flask_socketio import SocketIO, emit
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import threading
import time

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
socketio = SocketIO(app)

def scrape_and_emit():
    MARKET_RATE_URL = os.getenv('MARKET_RATE_URL')
    try:
        page = requests.get(MARKET_RATE_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', {'class': 'table table-condensed table-striped'})
        if table:
            rows = table.find("tbody").find_all("tr")
            data = []
            for row in rows:
                cells = row.find_all("td")
                currency = cells[0].text.strip()
                rate = cells[1].text.strip().replace('\u20a6', '')
                date = cells[2].text.strip()
                data.append({"Currency": currency, "Rate": str(rate), "Date": date})
            socketio.emit('data', data)
        else:
            socketio.emit('error', 'Table not found')
    except Exception as e:
        socketio.emit('error', f'Error: {str(e)}')

def background_scrape():
    while True:
        scrape_and_emit()
        time.sleep(120)  # Wait for 2 minutes

@socketio.on('connect')
def handle_connect():
    emit('message', 'Connected to the WebSocket server')

if __name__ == '__main__':
    threading.Thread(target=background_scrape, daemon=True).start()
    socketio.run(app, debug=True)