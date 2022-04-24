from bottle import post, request, redirect
import uuid
import re
import g
import time
from time import gmtime, strftime
import pymysql

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

##############################
@post("/signup")
def _():
    ### DEFINE VARIABLES ###
    user_id = str(uuid.uuid4())
    user_first_name = request.forms.get("user_first_name")
    user_last_name = request.forms.get("user_last_name")
    user_nick_name = request.forms.get("user_nick_name")
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")
    user_created_at = strftime("%a, %d %b %Y %H:%M", gmtime())

    user = {
    "user_id":user_id, 
    "user_first_name":user_first_name, 
    "user_last_name":user_last_name, 
    "user_nick_name":user_nick_name, 
    "user_email":user_email,
    "user_password":user_password,
    "user_created_at":user_created_at
    }

    ### VALIDATE ###
    user_id, error_id = g._is_uuid4(user_id)
    if error_id : return g._send(400, error_id)
    user_first_name, error_fn = g._is_item_textshort(user_first_name)
    if error_fn : return g._send(400, error_fn)
    user_last_name, error_ln = g._is_item_textshort(user_last_name)
    if error_ln : return g._send(400, error_ln)
    user_nick_name, error_nn = g._is_item_textmedium(user_nick_name)
    if error_nn : return g._send(400, error_nn)
    user_email, error_e = g._is_item_email(user_email)
    if error_e : return g._send(400, error_e)
    user_password, error_pw = g._is_item_textlong(user_password)
    if error_pw : return g._send(400, error_pw)

    print("user:")
    print(user)    
    try:
        print("production mode")
        import production
        db_config = g.DB_PROD

    except Exception as ex:
        print("development mode")
        print(ex)
        db_config = g.DB_DEV

        ### EMAIL - only in development mode ###
        sender_email = "szangyiwebdev@gmail.com"
        receiver_email = user_email
        # password = g.EMAIL_PW
        password = g.APP_PW

        message = MIMEMultipart("alternative")
        message["Subject"] = "Your new Tweeter account"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = """\
        Hey,

        Thank you for creating an account on Twetter.
        Enjoy!
        Tweeter
        """

        html = """\
        <html>
            <body>
            <p>
                Hey,<br>
                Thank you for creating an account on Twetter.
                <h2>Enjoy!</h2>
                <em>Twetter</em>
            </p>
            </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as ex:
                print("-----error")
                print(ex) 

    try:
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        # db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        # cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output
        
        sql = """INSERT INTO users (user_id, user_first_name, user_last_name, user_nick_name, user_email, user_password, user_created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        var = (user_id, user_first_name, user_last_name, user_nick_name, user_email, user_password, user_created_at)
            
        cur.execute(sql, var)
        db.commit()
        print("user created successfully", user)


       
    except Exception as ex:
        print("error:")
        print(ex)
    finally:
        db.close()
    return redirect("/login?success=signup_success")
    

  