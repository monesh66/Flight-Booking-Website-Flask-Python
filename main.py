from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
import mysql.connector
import datetime



database = mysql.connector.connect(host = "localhost",
                                   user = "root",
                                   password = "123123",
                                   database = "flight_booking_website")
db = database.cursor()

app = Flask(__name__,static_url_path='/static')

app.secret_key = '%KCP{NB@^f7idgf87rfg34768P:?tggjykO;ppip>Uk}'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#==================================== /home page =================================================
@app.route('/')
@app.route('/home')
def home():
    if not session.get("username"):
        print("1")
        return render_template('home.html',username="User",logined=0)
    
    elif session.get("username") != "Null":
        print("3")
        username = session.get("username")
        login_status = 1
        
    return render_template('home.html',logined = login_status,username = username)


#=================================== /sign-up ====================================================
@app.route('/sign-up',methods=['POST','GET'])
def signup():
     if request.method == 'POST':
            
        #get data from client using POST method
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']

        
        
        # list conveter
        email_list = list(email)

        
        # check for same username in database         
        db.execute("SELECT USERNAME FROM USER_DETAILS WHERE USERNAME='{0}';".format(username))
        db_username = db.fetchall()
        if db_username == []:
            username_found = 0           
        else:
            username_found = 1

            
        #check for same email in database
        db.execute("SELECT EMAIL FROM USER_DETAILS WHERE EMAIL='{0}';".format(email))
        db_email = db.fetchall()
        if db_email == []:
            email_found = 0
        else:
            email_found = 1
        
        
        # VALIDATOR
        # usename validator
        if username == "":
            flash("Username can't be empty")
            return render_template('sign_up.html')
        
        elif len(username) < 3 or len(username) > 16:
            flash("Username should be 8 - 15 character long")
            return render_template('sign_up.html')
        
        elif username_found == 1:
            flash("Username already taken!. Please try using another name")
            return render_template('sign_up.html')
        
        
        # email validator
        elif email == "":
            flash("Email can't be empty")
            return render_template('sign_up.html')
        
        elif len(email) < 12 or len(email) > 65:
            flash("Email should be 12 - 64 character long")
            return render_template('sign_up.html')
        
        elif email_list[-1] != "m" or email_list[-2] != "o" or email_list[-3] != "c" or email_list[-4] != "." or email_list[-5] != "l" or email_list[-6] != "i" or email_list[-7] != "a" or email_list[-8] != "m"  or email_list[-10] != "@":
            flash("Inavlid Email address")
            return render_template('sign_up.html')
        
        elif email_found == 1:
            flash("Email already Used!. Please login")
            return render_template('sign_up.html')
        
        # password validator
        elif len(password) < 8 or len(password) > 24:
            flash("Password should be 8 - 24 character long")
            return render_template('sign_up.html')
        
        #check for password and confirm password are same
        elif password != cpassword:
            flash("your password does not match confirm password")
            return render_template('sign_up.html')
        
        
        else:
            # store info in database

            db.execute("INSERT INTO USER_DETAILS(USERNAME,EMAIL,PASSWORD) VALUES('{0}','{1}','{2}');".format(username,email,password))
            database.commit()
            flash("Green")


            return redirect(url_for('login'))
        
        
     return render_template('sign_up.html')


#=================================== /login ====================================================
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        
        #get data from client using POST method
        username = request.form['username']
        password = request.form['password']


        #get user name and password from database
        db.execute("SELECT USERNAME FROM USER_DETAILS WHERE USERNAME='{0}';".format(username))
        db_username = db.fetchall()
        if db_username == []:
            username_found = 0
        else:
            db.execute("SELECT PASSWORD FROM USER_DETAILS WHERE USERNAME='{0}';".format(username))
            db_password = db.fetchone()
            username_found = 1


        if username == "":
            flash("Username can't be empty")
            return render_template('login.html')
        elif password == "":
            flash("Password can't be empty")
            return render_template('login.html')
        elif username_found == 0:
            flash("Username not found")
            return render_template('login.html')
        elif password != db_password[0]:
            flash("Invalid password for the usrename")
            return render_template('login.html')
        else:
            session["username"] = username
            return redirect(url_for('home'))
        


    return render_template('login.html')

 #====================================== /logout ===================================
@app.route('/logout')
def logout():
    session["username"] = None
    return redirect(url_for('home'))


 #====================================== /flight-redirect ===================================
@app.route('/flight-redirect',methods=['POST'])
def data_to_url():
    
    url = "http://localhost:5000/flight/"
    
    From = request.form['From']
    To = request.form['To']
    Date = request.form['Date']
    
    db.execute("SELECT ID FROM AIRPORT_NAME_ID WHERE NAME = '{0}';".format(From))
    departure_airport_id = db.fetchone()
    
    db.execute("SELECT ID FROM AIRPORT_NAME_ID WHERE NAME = '{0}';".format(To))
    aravial_airport_id = db.fetchone()
    
    
    url = str(url) + str(departure_airport_id[0])+ "-" +str(aravial_airport_id[0]) + "-" + str(Date)
    
    
    
    
    return redirect(url, code=302)
    
    



#====================================== /flight ===================================
@app.route('/flight')
def book_now():
    #/flight/CHI-TRI-10-07-2023/12341
    if not session.get("username"):
        flash("Login to access")
        return render_template('login.html',username="User",logined=0)

    else:
        print("3")
        username = session.get("username")
        login_status = 1
        departure_airport = ["Chennai International Airport","Coimbatore International Airport","Madurai International Airport","Tiruchirapalli International Airport"]
        aravial_airport = ["Chennai International Airport","Coimbatore International Airport","Madurai International Airport","Tiruchirapalli International Airport"]
        
        db.execute("SELECT NAME FROM AIRPORT_NAME_ID")
        departure_airport = db.fetchall()
        aravial_airport = departure_airport


        return render_template('book_now.html',username=username,logined=login_status,departure_airport=departure_airport,aravial_airport=aravial_airport)






@app.route('/flight/<search>')
def search(search):
    
    if not session.get("username"):
        flash("Login to access")
        return render_template('login.html',username="User",logined=0)
    
    else:
        username = session.get("username")
        login_status = 1
        departure_id = search[0:3]
        aravial_id = search[4:7]
        date = search[8:]
    
        db.execute("SELECT NAME FROM AIRPORT_NAME_ID WHERE ID='{0}';".format(departure_id))
        departure_airport = db.fetchone()
    
        db.execute("SELECT NAME FROM AIRPORT_NAME_ID WHERE ID='{0}';".format(aravial_id))
        aravial_airport = db.fetchone()
        x = datetime.datetime(int(search[8:12]),int(search[13:15]),int(search[16:18]))
    
        date1 = str(x.strftime("%d"))+" ("+str(x.strftime("%A"))+") "+str(x.strftime("%B"))+" "+str(x.strftime("%Y"))
    
    
    

    
        #data = [['Indigo Airline','12:30','3:30','3 Hrs','9,999','{0}/1002'],['Air India','12:50','2:30','1.5 Hrs','7,568','{0}/1003'],['Air India Express','12:30','3:30','3 Hrs','9,999','{0}/1002'],['Vistra Airline','12:50','2:30','1.5 Hrs','7,568','{0}/1003']]
    
        db.execute("SELECT NAME, DEPARTURE_TIME, ARRIVAL_TIME,DURATION,RATE,ID FROM FLIGHT WHERE DEPARTURE_AIRPORT_ID='{0}' AND ARRIVAL_AIRPORT_ID='{1}' AND DATE='{2}';".format(departure_id,aravial_id,date))
        data = db.fetchall()
        print(data)
        datas = []
        for i in data:
            a = list(i)
            a[5] = str(search) +"/"+ str(a[5])
            datas.append(a)
            print(datas)
        nul = "0"
        if data == []:
            nul = "1"
     
    
        return render_template('flight_list.html',username=username,logined=login_status,departure_airport=departure_airport[0],aravial_airport=aravial_airport[0],date = date1,datas=datas,nul=nul)








@app.route('/flight/<search>/<flight_id>',methods=['GET','POST'])
def flight_page(search,flight_id):
    
    if request.method == "GET":
        if not session.get("username"):
            flash("Login to access")
            return render_template('login.html',username="User",logined=0)
    
        else:
            username = session.get("username")
            login_status = 1
        
            db.execute("SELECT DEPARTURE_AIRPORT_ID,ARRIVAL_AIRPORT_ID, DEPARTURE_TIME,ARRIVAL_TIME,DURATION FROM FLIGHT WHERE ID='{0}';".format(flight_id))
            data = db.fetchone()
            print(data)
            url="http://localhost:5000/flight/"+str(search)+"/"+str(flight_id)
        
        
            return render_template('flight_book.html',username=username,logined=login_status,data=data,url=url)
        
        
    else:
        username = session.get("username")
        num = int(request.form['lol'])
        print(username,flight_id,num)
        
        db.execute("SELECT DEPARTURE_AIRPORT_ID,ARRIVAL_AIRPORT_ID,DEPARTURE_TIME,ARRIVAL_TIME,DATE,DURATION FROM FLIGHT WHERE ID='{0}';".format(flight_id))
        data = db.fetchone()
        
        db.execute("SELECT NAME FROM AIRPORT_NAME_ID WHERE ID='{0}';".format(data[0]))
        dep = db.fetchone()
        
        db.execute("SELECT NAME FROM AIRPORT_NAME_ID WHERE ID='{0}';".format(data[1]))
        arr = db.fetchone()
        
        
        db.execute("INSERT INTO TICKET(PASSANGER,ID,USERNAME,DEPARTURE_AIRPORT,ARRIVAL_AIRPORT, DEPARTURE_TIME,ARRIVAL_TIME,DATE,DURATION) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(num,flight_id,username,dep[0],arr[0],data[2],data[3],data[4],data[5]))
        database.commit()
        
        return redirect("http://localhost:5000/my-tickets", code=302)
        
        
    
    
    
    
    
    
    
    
    return flight_id




@app.route('/my-tickets')
def g():
    if not session.get("username"):
            flash("Login to access")
            return render_template('login.html',username="User",logined=0)
    
    else:
        username = session.get("username")
        login_status = 1
        
        db.execute("SELECT * FROM TICKET WHERE USERNAME = '{0}';".format(username))
        data = db.fetchall()
        
            
        
        
        return render_template('tickets.html',username=username,logined=login_status,datas=data)
    

#app.run(debug=True, port=5001)


#if __name__ == "__main__":
 #   app.run(debug=True)