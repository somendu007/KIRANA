# KIRANA - Online Grocery Store Web Application
This is an Online Grocery Store Web Application built using the Flask web framework. The app allows users to browse, search, and purchase grocery items, while administrators can manage products, categories, and orders. Below are the steps to set up and run the app.

# Getting Started
## Prerequisites
Python 3.x

Virtualenv (for creating a virtual environment)

# Installation
## Create a virtual environment and activate it:
virtualenv venv

source venv/bin/activate 

 On Windows, use venv\Scripts\activate

## Install the required packages:
pip install -r requirements.txt

# Usage
## Start the Flask app:
python app.py
## Open a web browser and navigate to http://127.0.0.1:5000 to access the app.

# Technologies Used
Flask
SQLite
HTML/CSS
Jinja2
Flask-WTF
Flask-Session

# Project Structure
The project follows this directory structure:

templates/: HTML templates
static/: Static files (CSS, JS, images)
app.py: Entry point for running the app

# Features
User registration and authentication
Product browsing and searching
Category display
Cart management
Order placement
Administrator functionalities for managing products and categories

