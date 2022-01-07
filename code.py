from flask import Flask, redirect, url_for, render_template, request
import requests


 #location of api
BASE = "http://papl.azurewebsites.net"

app = Flask(__name__)

@app.route("/")

def index():
    return redirect(url_for("submit"))
@app.route("/submit", methods=["POST", "GET"])

def submit():
    if request.method == "POST":
        weight = request.form["weight"]
        """Sender"""
        fromName = request.form["fromName"]
        fromStreet = request.form["fromStreet"]
        fromCode = request.form["fromCode"]
        fromCity = request.form["fromCity"]
        fromCountry = request.form["fromCountry"]
        """Receipient"""
        toName = request.form["toName"]
        toStreet = request.form["toStreet"]
        toCode = request.form["toCode"]
        toCity = request.form["toCity"]
        toCountry = request.form["toCountry"]
       
       
        data = {'weight': weight,
        'recipient':
        {
            'name' : fromName,
            'street' : fromStreet,
            'postalCode' : fromCode,
            'city' : fromCity,
            'country' : fromCountry
        },
        'sender':
        {
            'name' : toName,
            'street' : toStreet,
            'postalCode' : toCode,
            'city' : toCity,
            'country' : toCountry
        }
        }
        """Makes POST Request with application/json Media-Type"""
        r = requests.post(url = BASE + f"/parcel", json = data)
        
        return r.text        
    else:
        return render_template("submit.html")

@app.route("/track", methods=["POST", "GET"])

def track():
    if request.method == "POST":
        trackingId = request.form["trackingID"]
        r = requests.get(url = BASE + f"/parcel/{trackingId}")
        return r.text    
    else:
        return render_template("track.html")#

@app.route("/report", methods=["POST", "GET"])

def report():
    if request.method == "POST":
        trackingId = request.form["trackingID"]
        code = request.form["station"]
        checkbox = request.form.get('delivered') 
        
        if checkbox == "true":
            r = requests.post(url = BASE + f"/parcel/{trackingId}/reportDelivery")
            return r.text 
        else:
            r = requests.post(url = BASE + f"/parcel/{trackingId}/reportHop/{code}")
            return r.text             
    else:
        return render_template("report.html")

if __name__ == "__main__":
    app.run()

