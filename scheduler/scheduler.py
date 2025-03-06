from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests

app = Flask(__name__)
logger = app.logger
def trade_callback():
    logger.info(f"trade_callback called on {time.strftime("%Y-%m-%d %H:%M:%S")}")
    response = requests.get("")

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(trade_callback, 'interval', hours=1)
scheduler.start()

@app.route('/')
def trigger():
    return "The trader is running. It will sends the trade order to the trader every hour."

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()