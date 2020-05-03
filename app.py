from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create flask app
app = Flask(__name__)

#create connection to mongoDB
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_DB")

#render template for index html
@app.route("/")
def home():

    #find a select first intance of mars data in collection
    mars_data_entry = mongo.db.scrapped_info.find_one()

    #render the infomation on the html
    return render_template('index.html', mars = mars_data_entry )

#route to trigger scrape function
@app.route("/scrape")
def scrape():

    #store scrapped data
    mars_info = scrape_mars.scrape_info()

    #update the mongao databse: mars_DB with scrapped information
    mongo.db.scrapped_info.update({}, mars_info, upsert=True) 

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)