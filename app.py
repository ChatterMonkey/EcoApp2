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
rounded_startdate = 18273

print("time header: \n \n \n \n ")

seconds_since_epoch = round(time.time(),1)
print("seconds since epoch")
print(seconds_since_epoch)
print("days since epocj")
print(seconds_since_epoch/86400)

print("rounded start date")
print(rounded_startdate)
print("days since start")
print(seconds_since_epoch/86400 - rounded_startdate)




def print_user_data():


    c.execute("select * from userdata")
    result = c.fetchall()
    print(result)










# We can also close the cursor if we are done with it


print_user_data()




app = Flask(__name__) #create the Flask app



def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier








def log_login(userid):
    print("logging login...")
    rounded_time = round(time.time(),1)
    print(rounded_time)
    delta_t = round(rounded_time - seconds_since_epoch,1)
    print(seconds_since_epoch)
    print(delta_t)
    con = sqlite3.connect("database.db")
    con.cursor().execute("insert into home_record (userid, login_time) values(?,?)", (userid, delta_t))

    print("database content")
    print(sqlite3.connect("database.db").cursor().execute("select * from home_record").fetchall())
    con.commit()



def log_gift(userid):
    print("logging gift...")
    rounded_time = round(time.time(),1)
    print(rounded_time)
    delta_t = round(rounded_time - seconds_since_epoch,1)
    print(seconds_since_epoch)
    print(delta_t)
    con = sqlite3.connect("database.db")
    con.execute("insert into giftlog (userid, gift_claim_time) values(?,?)", (userid, delta_t))

    print("database content")
    print(sqlite3.connect("database.db").cursor().execute("select * from giftlog").fetchall())
    con.commit()






@app.route("/get_gift", methods=['Post'])
def returngift():

    userid = int(request.form.get("userid"))
    print("recieved user id")
    print(userid)
    connection = sqlite3.connect("database.db")
    c = connection.cursor()


    print("gift taking log:")
    print(c.execute("select * from giftlog ").fetchall())




    delta_t = c.execute("select gift_claim_time  from giftlog where userid = ? order by rowid desc limit 1", (userid,)).fetchall()
    connection.commit()
    print("time of last enrty")





    try:
        time_since_last_load = round(time.time()-seconds_since_epoch-delta_t[0][0],1)
        print(time_since_last_load)
    except IndexError:
        return "show"


    if time_since_last_load > seconds_between_gifts:
        return "show"


    return "hide"


















@app.route("/")
def send_to_home():
    return redirect("/static/home.html")





@app.route("/get_daily_action_for_action_page", methods=['POST'])
def return_daily_challange_for_action_page():

    userid = request.form.get("userid")
    con = sqlite3.connect("database.db")


    print("actions so far:   \n \n")
    print(con.execute("select * from actionlog").fetchall())
    currentdate = truncate(time.time()/86400)
    delta_days = currentdate-rounded_startdate


    action_id = con.execute("select actionid from challangetable where challange_date=?", (delta_days,)).fetchall()
    print("today's challange is ")
    print(action_id)


     #check if the last time they proformed an action was less than 1 day ago
    delta_t = con.execute("select actiontimestamp  from actionlog where userid = ? and actionid = ? order by rowid desc limit 1", (userid, action_id[0][0],)).fetchall()
    try:
        time_since_last_action = delta_t[0][0]
    except IndexError:
        time_since_last_action = 86401
    if time_since_last_action > 86400:
        print("IT HAS BEEN MORE THAN A DAY SINCE ACTION WAS ALST COMPLETED \n \n \n \n ")

    else:
        print("REWARD ALREADY CLAIMED")
        return "0"











    action_message = con.execute("select action_message from action_table where actionid=?", (action_id[0][0],)).fetchall()
    print(action_message[0][0])
    action_massage_text = action_message[0][0]




    print(action_id)
    string = str(action_id[0][0])
    return string




@app.route("/register_action", methods=['POST'])
def register_action():

    action_id = int(request.form.get('actionid'))
    userid = int(request.form.get("userid"))
    print("action id is "+str(action_id))
    conn = sqlite3.connect("database.db")

    currentdate = truncate(time.time()/86400)
    delta_days = currentdate-rounded_startdate


    # regester action in actionlog

    print("logging action...")
    rounded_time = round(time.time(),1)
    print(rounded_time)
    delta_t = round(rounded_time - seconds_since_epoch,1)
    print(seconds_since_epoch)
    print(delta_t)
    conn.execute("insert into actionlog (userid, actionid, actiontimestamp) values(?,?,?)", (userid, action_id, delta_t,))
    conn.commit()
    print(conn.execute("select * from actionlog").fetchall())
    confrim_message = conn.execute("select action_message from action_table where actionid = ?", (action_id,)).fetchall()
    conn.commit()
    return confrim_message[0][0]



@app.route("/return_action_message", methods=['POST'])
def return_message():

    action_id = int(request.form.get('actionid'))

    print("action id is "+str(action_id))
    conn = sqlite3.connect("database.db")
    action_message = conn.execute("select action_message from action_table where actionid = ?", (action_id,)).fetchall()

    return action_message[0][0]





@app.route('/return_daily_challange', methods=['POST'])
def return_daily_challange():



    userid = request.form.get("userid")
    con = sqlite3.connect("database.db")


    print("actions so far:   \n \n")
    print(con.execute("select * from actionlog").fetchall())





    currentdate = truncate(time.time()/86400)
    delta_days = currentdate-rounded_startdate


    action_id = con.execute("select actionid from challangetable where challange_date=?", (delta_days,)).fetchall()
    print("today's challange is ")
    print(action_id)


     #check if the last time they proformed an action was less than 1 day ago
    delta_t = con.execute("select actiontimestamp  from actionlog where userid = ? and actionid = ? order by rowid desc limit 1", (userid, action_id[0][0],)).fetchall()
    try:
        time_since_last_action = delta_t[0][0]
    except IndexError:
        time_since_last_action = 86401
    if time_since_last_action > 86400:
        print("IT HAS BEEN MORE THAN A DAY SINCE ACTION WAS ALST COMPLETED \n \n \n \n ")

    else:
        print("REWARD ALREADY CLAIMED")
        return "Congratulations! You have completed today's challange."











    action_message = con.execute("select action_message from action_table where actionid=?", (action_id[0][0],)).fetchall()
    print(action_message[0][0])
    action_massage_text = action_message[0][0]

    print(action_id)
    string = "Receive double the points for today's challange:  " + str(action_massage_text)
    return string










@app.route('/post_login_data', methods=['POST'])
def verify_login():
    qusername = request.form.get('username')
    qpassword = request.form.get('password')
    try:
        int_qpassword = int(qpassword)
    except:
        response = {"status":"false", "message":"Incorrect username or password."}
        print(response)
        return response
    connection = sqlite3.connect("database.db")
    passwords = connection.cursor().execute("select password from userdata").fetchall()
    print(passwords)
    usernames = connection.cursor().execute("select username from userdata").fetchall()
    print(usernames)
    index = 0
    for name_in_tuple in usernames:
        if name_in_tuple[0] == qusername:
            print("we have a match")
            if passwords[index][0] == int_qpassword:
                real_password  =passwords[index][0]
                print("User logged in")
                con = connection.cursor()
                print(con.execute("select password from userdata ").fetchall())
                id = con.execute("select userid from userdata where password=?",(real_password,)).fetchall()
                print("id:")
                print(id)
                print(con.execute("select userid from userdata").fetchall())
                name = con.execute("select username from userdata where password=?",(real_password,)).fetchall()
                xp = con.execute("select ep from userdata where password=?",(real_password,)).fetchall()
                cc = con.execute("select challanges_competed from userdata where password=?",(real_password,)).fetchall()
                response = {"status":"true", "message":"congratulations! You are logged in", "id":id, "username":name, "xp":xp, "cc":cc }
                print(response)
                return response
        else:
            print("no match")
            index = index+1
    response = {"status":"false", "message":"Incorrect username or password."}
    return response
@app.route('/get_user_info', methods=['POST'])
def send_info():
    userid = request.form.get('userID')
    connection = sqlite3.connect("database.db")
    c = connection.cursor()
    print(userid)
    print(c.execute("select * from userdata where userid=1").fetchall())
    xp = c.execute("select ep from userdata where userid=?", (userid,)).fetchall()
    username = c.execute("select username from userdata where userid=?", (userid,)).fetchall()
    cc = c.execute("select challanges_competed from userdata where userid=?", (userid,)).fetchall()
    print("Ep value fort this user:    ")
    print(xp)
    response = {"username":username, "xp":xp, "cc":cc, "id":userid}
    print(response)
    return response

@app.route('/leader_board', methods=['GET'])
def send_leader_board():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    query = "select username,ep, challanges_competed from userdata order by ep desc"
    result = cursor.execute(query)

    items = []
    i = 0
    for row in result:
        items.append({'username':row[0], 'xp':row[1], 'cc':row[2]})
        i = i+1
    connection.close()
    board_json = json.dumps(items)
    loaded_json = json.loads(board_json)

    print(loaded_json[0]["xp"])

    return board_json










if __name__ == '__main__':
    app.run(debug=False, port=5000,host='0.0.0.0') #run app in debug mode on port 5000

