#!/bin/bash

# Run the main Python application
poetry run python3 app.py

poetry run mlflow ui 
