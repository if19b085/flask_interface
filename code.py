from flask import Flask, redirect, url_for, render_template, request
import requests
import json


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
        
        if(r.status_code == 201):
            jsonData = json.loads(r.json)
            return render_template('submitanswer.html', trackingId = jsonData['trackingId'])   
        else:
            return render_template('error400.html')   
    else:
        return render_template("submit.html")

@app.route("/track", methods=["POST", "GET"])

def track():
    if request.method == "POST":
        trackingId = request.form["trackingID"]
        r = requests.get(url = BASE + f"/parcel/{trackingId}")
        jsonData = json.loads(r.json)
        if(r.status_code == 200):
             #TODO: Parse stations out of r.text and give the parameters to page
            return render_template('trackanswer.html', messageData = jsonData)   
        elif(r.status_code == 400):
            return render_template('error400.html')
        elif(r.status_code == 404):
            return render_template('error404.html')   
    else:
        return render_template("track.html")

@app.route("/report", methods=["POST", "GET"])

def report():
    if request.method == "POST":
        trackingId = request.form["trackingID"]
        code = request.form["station"]
        checkbox = request.form.get('delivered') 
        
        if checkbox == "true":
            r = requests.post(url = BASE + f"/parcel/{trackingId}/reportDelivery")

            if(r.status_code == 200):
                return render_template('reportanswer.html', trackingId = trackingId)   
            elif(r.status_code == 400):
                 return render_template('error400.html')
            elif(r.status_code == 404):
                return render_template('error404.html') 
        else:
            r = requests.post(url = BASE + f"/parcel/{trackingId}/reportHop/{code}")

            if(r.status_code == 200):
                return render_template('reportanswer.html', trackingId = trackingId)   
            elif(r.status_code == 400):
                 return render_template('error400.html')
            elif(r.status_code == 404):
                return render_template('error404.html')             
    else:
        return render_template("report.html")
    

if __name__ == "__main__":
    app.run()

