from flask import Flask
import logging

def log_handling(app: Flask):
    logger = app.logger
    # Set the logger level (you can use DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.INFO)
    # Create a file handler
    file_handler = logging.FileHandler(f'{app.name}.log')
    file_handler.setLevel(logging.INFO)
    # Create a log format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    # Add the file handler to the app logger
    logger.addHandler(file_handler)
    return logger