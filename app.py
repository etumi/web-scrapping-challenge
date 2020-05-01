from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create flask app
app = Flask(__name__)

#create connection to mongoDB
mongo = PyMongo(app, uri="mongodb://localhost:27017/<databse name>")

#render template for index html
@app.route("/")
def home():

    #find a select first intance of mars data in collection
    selected_mars_data = mongo.db.collection.find_one()

    #render the infomation on the html
    return render_template('index.html', mars= selected_mars_data)

#route to trigger scrape function
@app.route("/scrape")
def scrape():

    #strore scrapped data
    mars_info = scrape_mars.scrape

    #update mondoDB with scrapped DB
    database_name = mongo.db.collection.update({}, mars_info, upsert=True) 

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)