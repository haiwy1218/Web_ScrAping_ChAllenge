# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time 
from pymongo import MongoClient

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = MongoClient(conn)

# create home route and define home function
@app.route('/')
def home():
    # Find one record of data from the mongo database
    mars_info = client.db.mars_collection.find_one()

    # Return template and data
    return render_template("index_scrape.html", mars_data=mars_info)

# create scrape route 
@app.route ('/scrape')
def scrape():
    # run the scrape function
    mars_data = scrape_mars.scrape()

    # insert the mars data in to the collection
    client.db.mars_collection.update({}, mars_data, upsert=True)

    # go back to the home page
    return redirect("/")

# run the app
if __name__ == "__main__":
    app.run(debug=True)