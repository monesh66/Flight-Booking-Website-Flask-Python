from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
import mysql.connector



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


#====================================== /book-now ===================================
@app.route('/flight')
def book_now():
    if not session.get("username"):
        flash("Login to access")
        return render_template('login.html',username="User",logined=0)

    else:
        print("3")
        username = session.get("username")
        login_status = 1
        departure_airport = ["Chennai International Airport","Coimbatore International Airport","Madurai International Airport","Tiruchirapalli International Airport"]

    return render_template('book_now.html',username=username,logined=login_status,departure_airport=departure_airport)


@app.route('/flight/<search>')
def search(search):
    return search




@app.route('/flight/<search>/<flight_id>')
def flight_page(search,flight_id):
    return flight_id








#if __name__ == "__main__":
 #   app.run(debug=True)