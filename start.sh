#!/bin/bash

# Run the main Python application
poetry shell

poetry run python3 app.py

poetry run mlflow ui 
