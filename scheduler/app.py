from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests

app = Flask(__name__)
logger = app.logger

# Initialize the scheduler
scheduler = BackgroundScheduler()

def trade_callback(trader_host: str, trader_port: int):
    logger.info(f"trade_callback called on {time.strftime('%Y-%m-%d %H:%M:%S')}")
    # Example URL construction; adjust as needed
    url = f"http://{trader_host}:{trader_port}/trader/execute"
    response = requests.get(url)
    logger.info(f"Response from trader: {response.status_code}")

@app.route('/<trader_host>/<int:trader_port>/')
def trigger(trader_host, trader_port):
    # Add the job with the provided trader_host and trader_port
    scheduler.add_job(trade_callback, args=(trader_host, trader_port), trigger='interval', minutes=1)
    return "The trader is running. It will send the trade order to the trader every minute."

if __name__ == '__main__':
    try:
        scheduler.start()
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
