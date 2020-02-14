#app.py
#test
import random
from flask import Flask, request, render_template, redirect
from flask import jsonify
#import main Flask class and request object
import json
import time
coins = 0
import sqlite3
from flask import url_for, redirect
from collections import OrderedDict
connection = sqlite3.connect("database.db")
c = connection.cursor()



seconds_between_gifts = 20




data = c.execute("select * from challangetable").fetchall()
print(data)

# Save (commit) the changes

print(c.execute("select * from challangetable").fetchall())
#startdate = time.time()/86400
#rounded_startdate = round(startdate, 2)
#print(rounded_startdate)





app = Flask(__name__) #create the Flask app








@app.route("/")
def send_to_home():
    return redirect("/static/home.html")




if __name__ == '__main__':
    app.run(debug=False, port=5000,host='0.0.0.0') #run app in debug mode on port 5000

