from flask import Flask, redirect, url_for, render_template, request
from dotenv import load_dotenv
import urllib.parse
from pymongo import MongoClient
import os
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv()

# thanks literally everyone for not making nodejs style module support
DATABASE_NAME = "snaps"
client = MongoClient()
db = client[DATABASE_NAME]
snaps_collection = db.snaps
def __init__():
    try:
        client = MongoClient()
        db = client[DATABASE_NAME]
        snaps_collection = db.snaps
    except:
        print("PLEASE SET UP A DATABSE")
        quit()

# Redirect everything to the github page because we don't have a home page
@app.route('/')
def index():
    return redirect("https://github.com/itsmingjie/claps")

# the good stuff
@app.route('/snap', methods=['POST'])
@cross_origin()
def snap():
    url = urllib.parse.quote(urllib.parse.urlparse(request.form['url']).path).replace("/", "")
    num_snaps = int(request.form['num_snaps'])
    # check if document exsists already
    if snaps_collection.find_one({"url":url}) != None:
        new_num_snaps = snaps_collection.find_one({"url":url})["num_snaps"] + num_snaps
        snaps_collection.find_one_and_update(
            {"url":url},
            {"$set":
                {"num_snaps": new_num_snaps}
            },upsert=True
        )
    else:
        new_num_snaps = num_snaps
        snaps_collection.insert_one({"url":url, "num_snaps":new_num_snaps})
    print(snaps_collection.find_one({"url":url}))
    return str(new_num_snaps)

# api to get information about an article - DEPRECATED - JUST USE /snap with 0 for num_snaps
@app.route('/get_snaps', methods=['GET'])
@cross_origin()
def get_snaps():
    url = urllib.parse.quote(urllib.parse.urlparse(request.form['url']).path)
    # find document with matching url and return it
    return snaps_collection.find_one({"url":url})

if __name__ == '__main__':
    app.run()
