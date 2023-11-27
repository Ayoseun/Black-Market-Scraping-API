import asyncio
import os
import requests
import websockets
from flask import Flask
from flask_socketio import SocketIO, emit
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
async def handler(websocket, path):
    while True:
        await scrape_and_emit(websocket)
        await asyncio.sleep(3)  # Wait for 2 minutes

start_server = websockets.serve(handler, "localhost", 8000)

async def scrape_and_emit(websocket):
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
         
            await websocket.send(str(data))
        else:
             await websocket.send("error")
    except Exception as e:
        
         await websocket.send(f'Error: {str(e)}')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()