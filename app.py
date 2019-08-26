from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app,uri = "mongodb://localhost:27017/mars")

@app.route('/')

def index():
    mars_dict = mongo.db.marsdetails.find_one()

    # mars_dict = scrape_mars.scrape()

    return render_template("index.html",mars_dict = mars_dict)


@app.route('/scrape')

def scrape():

    mars_qry = scrape_mars.scrape()

    mongo.db.marsdetails.update({},mars_qry,upsert = True)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug = True)